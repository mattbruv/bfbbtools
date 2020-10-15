from files import *
from parseasm import *
import os.path
import subprocess

def getCPPPath(path):
    return Path(str(path).replace("asm\\", "src\\").replace(".s", ".cpp"))

def updateMake(path):
    spath = str(path)
    makePath = "../bfbbdecomp/obj_files.mk"
    makeText = open(makePath).readlines()
    for i in range(0, len(makeText)):
        line = makeText[i]
        if path.name.replace(".s", ".o") in line:
            add = line.replace("asm/", "src/")
            makeText[i] = line + add
    open(makePath, "w").writelines(makeText)

def processFile(path):

    if "Game" not in str(path) and "Core" not in str(path):
        return

    cppPath = getCPPPath(path)

    if not os.path.exists(cppPath):
        #print(cppPath, path, "does not exist")
        return
    
    # if the CPP file has shit in it, don't overwrite it
    if len(open(cppPath).readlines()) > 1:
        return

    asmText = open(path).read()
    asmBlocks = parseAsm(path)
    if ".text" not in asmBlocks:
        return

    print(path)
    textBlock = asmBlocks[".text"]
    lastLine = textBlock.splitlines()[-1:][0]
    padding = 1
    if lastLine == "":
        padding = 0
    asmText = asmText.replace(textBlock, "".join([".if 0\n\n", textBlock, ("\n" * padding), ".endif\n\n"]))
    open(path, "w").write(asmText)

    # write to file
    subprocess.run(["python", "inlineasm.py", path.name])
    updateMake(path)


a = getAsmFiles()
test = a[15]
processFile(test)

#for test in a:
#    processFile(test)