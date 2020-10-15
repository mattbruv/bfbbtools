import json
from files import *
from parseasm import *
from demangle import demangleFunction
from inline.helpers import getAsmFunctions

asmFiles = getAsmFiles()

funcDict = {}

#print(demangleFunction("YUV_blit__FPvUlUlUlT0UlUlUlUlUlUlUlT0P5BLITS"))
#exit(1)
i = 0

for f in asmFiles:
    blocks = parseAsm(f)
    if ".text" not in blocks:
        continue
    text = blocks[".text"]
    fs = getAsmFunctions(text)
    print(f, len(fs), "functions")
    for func in fs:
        func = func.replace(":", "")
        realname = None
        try:
            realname = demangleFunction(func)
        except:
            realname = None
        if func not in funcDict and realname != None and func != realname:
            funcDict[func] = realname

open("demangled.json", "w").write(json.dumps(funcDict, indent=4))