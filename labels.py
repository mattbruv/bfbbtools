from symbols import *
from files import *
from match import matchLabels

symbols = getSymbols()

ignore_lbl_files = [
    "init.s",
    "Runtime.s"
]

def blacklistedAddrs():
    asm = getAsmFiles()
    addrs = []
    for a in asm:
        if a.name in ignore_lbl_files:
            data = open(a).read()
            addrs += list(matchLabels(data))
    return set(addrs)

def renameGlobalLabels():
    asm = getAsmFiles()
    names = set()
    count = 0
    filecount = 0
    blacklist = blacklistedAddrs()

    for f in asm: # iterate assembly files
        if f.name in ignore_lbl_files: # but not excluded ones
            continue

        filecount += 1
        data = open(f).read()
        matches = matchLabels(data)
        replacements = 0

        for lbl in matches: # loop through every label in the file
            name = getFunctionName(lbl) # name is None if not in symbol table
            if name is not None and lbl not in blacklist:
                if not isValidName(name): # test for mangled c++ name
                    # if  mangled, add a comment above the global definition
                    data = data.replace(".global lbl_" + lbl, "/* " + name + " */\n.global lbl_" + lbl)
                    print("sanitized", name)
                    name = sanitize(name)
                # replace the label with name from symbol file
                data = data.replace('lbl_' + lbl, name)
                replacements += 1
                names.add(name)
        count += replacements
        print(f, "replaced", replacements, "labels")
        open(f, 'w').write(data) # write new assembly file changes
    print("Replaced", count, "references of",  len(names), "unique global labels across", filecount, "files.")

syms = list(filter(lambda x: x["type"] == "OBJECT" and x["scope"] == "GLOBAL", symbols))

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

renameGlobalLabels()