from symbols import *
from files import *
from match import matchFuncs

symbols = getSymbols()

ignore_func_files = [
    "init.s",
    "Runtime.s"
]

whitelist = [
    "\\Game\\",
    "\\Core\\",
    "\\bink\\",
    "\\ODEGdev",
    #"\\rwsdk\\", # fails
    "\\dolphin\\", 
#    "\\CodeWarrior", # also fails
    "asm\\bss.s",
    "asm\\ctors.s",
    "asm\\data.s",
    "asm\\dtors.s",
    "asm\\extab.s",
    "asm\\extabindex.s",
    "asm\\init.s", 
    "asm\\rodata.s",
    "asm\\sbss.s",
    "asm\\sbss2.s",
    "asm\\sdata.s",
    "asm\\sdata2.s",
]

def inWhitelist(p):
    for w in whitelist:
        if w in p:
            return True
    return False

for asm in getAsmFiles():
    p = asm.__str__()
    if not inWhitelist(p):
        ignore_func_files.append(asm.name)
for f in ignore_func_files:
    print("ignore", f)

def blacklistedAddrs():
    asm = getAsmFiles()
    addrs = []
    for a in asm:
        if a.name in ignore_func_files:
            data = open(a).read()
            addrs += list(matchFuncs(data))
    return set(addrs)

def renameLocalFuncs():
    asm = getAsmFiles()
    names = set()
    count = 0
    filecount = 0
    blacklist = blacklistedAddrs()
    invalid = []

    for f in asm: # iterate assembly files
        if f.name in ignore_func_files: # but not excluded ones
            continue

        filecount += 1
        data = open(f, newline='').read()
        matches = matchFuncs(data)
        replacements = 0

        for func in matches: # loop through every label in the file
            name = getFunctionName(func) # name is None if not in symbol table
            if name is not None and func not in blacklist:
                if not isValidName(name): # test for mangled c++ name
                    # if  mangled, add a comment above the global definition
                    data = data.replace(".global func_" + func, "/* " + name + " */")
                    invalid += [func, f, name]
                    print("sanitized", name)
                    name = sanitize(name)
                # replace the label with name from symbol file
                else:
                    data = data.replace('.global func_' + func + "\n", '')
                data = data.replace('func_' + func, name)
                replacements += 1
                names.add(name)
        count += replacements
        if replacements > 0:
            print(f, "replaced", replacements, "labels")
        open(f, 'w', newline='').write(data) # write new assembly file changes
    print("Replaced", count, "references of",  len(names), "local functions across", filecount, "files.")

syms = list(filter(lambda x: x["type"] == "FUNC" and x["scope"] == "LOCAL", symbols))

# hash map to speed up label lookups
lookupDict = {}

for s in syms:
    addr = s["address"]
    if addr not in lookupDict:
        lookupDict[addr] = s
    else:
        # this should never be reachable
        exit(1)


def getFunctionName(address):
    if address not in lookupDict:
        return None
    return lookupDict[address]["name"]

renameLocalFuncs()