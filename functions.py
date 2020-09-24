from symbols import *
from files import *
from match import *

symbols = getSymbols()

ignore_func_files = [
    "init.s",
    "Runtime.s"
]

def blacklistedAddrs():
    asm = getAsmFiles()
    addrs = []
    for a in asm:
        if a.name in ignore_func_files:
            data = open(a).read()
            addrs += list(matchFuncs(data))
    return set(addrs)

def renameGlobalFunctions():
    asm = getAsmFiles()
    names = set()
    count = 0
    filecount = 0
    blacklist = blacklistedAddrs()
    for f in asm:
        if f.name in ignore_func_files:
            continue
        filecount += 1
        data = open(f).read()
        matches = matchFuncs(data)
        replacements = 0
        for func in matches: 
            name = getFunctionName(func)
            if name is not None and func not in blacklist:
                if not isValidName(name):
                    data = data.replace(".global func_" + func, "/* " + name + " */\n.global func_" + func)
                    print("sanitized", name)
                    name = sanitize(name)
                data = data.replace('func_' + func, name)
                replacements += 1
                names.add(name)
        count += replacements
        print(f, "replaced", replacements, "symbols")
        open(f, 'w').write(data)
    print("Replaced", count, "references of",  len(names), "unique functions across", filecount, "files.")

def getFunctionName(address):
    syms = list(filter(lambda x: x["type"] == "FUNC" and x["scope"] == "GLOBAL" and x["address"] == address, symbols))
    if len(syms) > 1:
        print("ERROR", address, "HAS MULTIPLE REFS")
        exit(69)
    if len(syms) == 0:
        return None
    return syms[0]["name"]

renameGlobalFunctions()