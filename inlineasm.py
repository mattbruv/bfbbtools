import argparse
from files import getAsmFiles
from inline.helpers import *
from path import asmToSrcPath
import json
from demangle import demangleFunction
from parseasm import parseAsm

desc = "Automatically move and inline assembly into CPP files"
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("asmFile", help="The assembly file to process")
parser.add_argument("-l", "--link", help="Reference the new src file in obj_files.mk", action="store_true")

def getSource(name):
    files = list(filter(lambda x: name.lower() in x.name.lower(), getAsmFiles()))
    if len(files) > 1:
        print("Error: Ambiguous filename:", name)
        print("Please specify filename in greater detail.")
        for f in files:
            print(f)
        quit()
    if len(files) == 0:
        print("Error: No files including", name)
        quit()
    return files[0]

typeList = json.loads(open("types.json").read())
mangledDict = json.loads(open("demangled.json").read())

def format(c, f, path, namespace=False):
    c += "\n"

    if f in mangledDict:
        c += "// " + mangledDict[f] + "\n"
    #if f in typeList:
    #    c+= "// " + typeList[f] + "\n"
    if namespace:
        c += "namespace {\n"
    c += "#pragma GLOBAL_ASM(\"" + path + "\", \""
    c += f + "\")\n"
    if namespace:
        c += "}\n"
    return c

def run():
    args = parser.parse_args()
    sourceFile = getSource(args.asmFile)
    blocks = parseAsm(sourceFile)

    out = str(sourceFile).replace("asm\\", "src\\").replace(".s", ".cpp")

    name = sourceFile.name.replace(".s", ".h")
    code = '#include "' + name + '"\n'
    code += "\n#include <types.h>\n"
    funcs = getAsmFunctions(blocks[".text"])
    for f in funcs:
        isLocal = False
        if "global " + f.replace(":", "") in blocks[".text"]:
            isLocal = False
        p = str(sourceFile)[14::].replace('\\', '/')
        code = format(code, f.replace(':', ''), p, namespace=isLocal)
        pass
    open(out, "w", newline='').write(code)

run()