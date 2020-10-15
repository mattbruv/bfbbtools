import json
from files import *
from parseasm import *
from demangle import demangleFunction
from inline.helpers import getAsmFunctions

asmFiles = getAsmFiles()

funcDict = json.loads(open("demangled.json").read())
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
        if func in funcDict:
            continue
        realname = None
        try:
            realname = demangleFunction(func)
        except:
            realname = None
        if func not in funcDict and realname != None and func != realname:
            funcDict[func] = realname
            print(func, realname)

open("demangled.json", "w").write(json.dumps(funcDict, indent=4))