import argparse
from inline.helpers import *
from path import path

desc = "Automatically move and inline assembly bytes into CPP files"
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("asmFile", help="The assembly file to process")
parser.add_argument("-l", "--link", help="Reference the new src file in obj_files.mk", action="store_true")

def run():
    args = parser.parse_args()
    sourceFile = getSource(args.asmFile)
    asm = open(sourceFile, "r").read()
    
    cppPath = sourceFile.__str__().replace('asm', 'src').replace('.s', '.cpp')
    print(cppPath)
    source = ""

    fs = getAsmFunctions(asm, strip=True)
    source = writeFunctions(source, fs)

    for func in fs:
        lines = getAsmFunctionBlock(asm, func)
        code = blockToBytes(lines)
        source = writeCode(source, func, code)

    open(cppPath, "w").write(source)
    #data = open(path + "obj_files.mk").read()
    #print(data)
    #print(sourceFile)

run()