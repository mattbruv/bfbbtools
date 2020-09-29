import argparse
from files import getAsmFiles
from inline.helpers import *
from path import asmToSrcPath

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

def format(c, f, path):
    c += "\n"
    c += "#pragma GLOBAL_ASM(\"" + path + "\", \""
    c += f + "\")\n"
    return c

def run():
    args = parser.parse_args()
    sourceFile = getSource(args.asmFile)
    asm = open(sourceFile, "r").read()

    out = str(sourceFile).replace("asm\\", "src\\").replace(".s", ".cpp")

    name = sourceFile.name.replace(".s", ".h")
    code = '#include "' + name + '"\n'
    funcs = getAsmFunctions(asm)
    for f in funcs:
        p = str(sourceFile)[14::].replace('\\', '/')
        code = format(code, f.replace(':', ''), p)
        pass
    open(out, "w").write(code)

run()