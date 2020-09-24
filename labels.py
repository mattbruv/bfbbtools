from symbols import *
from files import *
from match import matchLabels

symbols = getSymbols()

ignore_lbl_files = [
    "init.s",
    "Runtime.s"
]

def getLabels():
    return list(filter(lambda x: x["type"] == "OBJECT" and x["scope"] == "GLOBAL", symbols))

def getFuncs():
    return list(filter(lambda x: x["type"] == "OBJECT" and x["scope"] != "GLOBAL", symbols))

fnames = list(map(lambda x: x["name"], getFuncs()))

"""
for lbl in getLabels():
    if lbl["name"] in fnames:
        print(lbl["name"])
"""


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
    for f in asm:
        if f.name in ignore_lbl_files:
            continue
        filecount += 1
        data = open(f).read()
        matches = matchLabels(data)
        replacements = 0
        for lbl in matches: 
            name = getFunctionName(lbl)
            if name == "LastState":
                continue
            if name is not None and lbl not in blacklist:
                if not isValidName(name):
                    data = data.replace(".global lbl_" + lbl, "/* " + name + " */\n.global lbl_" + lbl)
                    print("sanitized", name)
                    name = sanitize(name)
                data = data.replace('lbl_' + lbl, name)
                replacements += 1
                names.add(name)
        count += replacements
        print(f, "replaced", replacements, "labels")
        open(f, 'w').write(data)
    print("Replaced", count, "references of",  len(names), "unique global labels across", filecount, "files.")

def getFunctionName(address):
    syms = list(filter(lambda x: x["type"] == "OBJECT" and x["scope"] == "GLOBAL" and x["address"] == address, symbols))
    if len(syms) > 1:
        print("ERROR", address, "HAS MULTIPLE REFS")
        exit(69)
    if len(syms) == 0:
        return None
    return syms[0]["name"]

renameGlobalLabels()

#print(blacklistedAddrs())
#a = "render_fill_rect__FRC13basic_rect<f>10iColor_tag"