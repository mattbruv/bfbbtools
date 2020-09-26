import argparse
from files import getAsmFiles
from inline.helpers import *
from path import asmToSrcPath

desc = "Automatically move and inline assembly into CPP files"
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("asmFile", help="The assembly file to process")
parser.add_argument("-l", "--link", help="Reference the new src file in obj_files.mk", action="store_true")
#parser.add_argument("-d", '--defineTop', help="Define all symbols at one spot at top of the C++ file, as apposed to above each function", action="store_true")
#parser.add_argument("--toggle", help="Include a #DEFINE to toggle between assembly and cpp")

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

def run():
    args = parser.parse_args()
    sourceFile = getSource(args.asmFile)
    asm = open(sourceFile, "r").read()
    #asm = desanitize(asm)
    funcs = getAsmFunctions(asm)

    # collect all global labels
    labels = set()
    funcLabels = set()
    exclude = set(getLabels(asm, strip=True)) # function labels from this file

    for f in funcs:
        block = getAsmFunctionBlock(asm, f)
        lbls = getBlockLabels(block)
        fs = getBlockFunctionCalls(block)
        funcLabels.update(fs)
        labels.update(lbls)
    
    funcLabels = funcLabels - exclude
    externLabels = labels - funcLabels
    #print(externLabels)
    #print(sourceFile)
    cppsource = '#include "' + sourceFile.name.replace('.s', '.h') + '"' + "\n\n"
    extern = []

    extern.append("// Functions in " + sourceFile.name.replace('.s', '.cpp'))
    fileFuncs = getAsmFunctions(asm, strip=True)
    extern += list(map(funcString, fileFuncs))

    extern += ["", "// external function references"]
    fs = sorted(list(funcLabels))
    fs = list(map(funcString, fs))
    extern += fs

    extern += ["", "// assembly references"]
    lbls = sorted(list(externLabels))
    lbls = list(map(labelString, lbls))
    extern += lbls

    cppsource += externBlock(extern) + "\n"

    for f in funcs:
        block = getAsmFunctionBlock(asm, f)
        code = blockToCPP(f, block)
        cppsource += code + "\n"


    outPath = asmToSrcPath(sourceFile.__str__())
    open(outPath, "w", newline="").write(cppsource)

run()