from files import getAsmFiles
from parseasm import parseAsm
from helpers import getAsmFunctions, getAsmFunctionBlock, filterBlockCode


def isGameFile(path):
    s = str(path)
    return "Game\\" in s or "Core\\" in s


floatInstructions = sorted([
    "fadd",
    "fadds",
    "fsub",
    "fsubs",
    "fmul",
    "fmuls",
    "fdiv",
    "fdivs",
    "fres",
    "frsqrte",
    "fsel",
    "fmadd",
    "fmadds",
    "fmsub",
    "fmsubs",
    "fnmadd",
    "fnmadds",
    "fnmsub",
    "fnmsubs",
    "frsp",
    "fctiw",
    "fctiwz",
    "fcmpu",
    "fcmpo",
    "mffs",
    "mcrfs",
    "mtfsfi",
    "mtfsf",
    "mtfsb0",
    "mtfsb1",
    "fmr",
    "fneg",
    "fabs",
    "fnabs",
    "psq_lx",
    "psq_lux",
    "psq_stx",
    "psq_stux",
    "psq_l",
    "psq_lu",
    "psq_st",
    "psq_stu"
])

files = list(filter(isGameFile, getAsmFiles()))


def getShortestFuncs(dict, label, limit=20):
    funcs = dict[label]
    names = funcs.keys()
    result = sorted(names, key=lambda x: funcs[x])[:limit]
    return result


lookup = {}
addrs = {}

for f in floatInstructions:
    lookup[f] = {}

# loop through every game file
for f in files:
    blocks = parseAsm(f)
    if not ".text" in blocks:
        continue
    text = blocks[".text"]
    functions = getAsmFunctions(text)
    # loop through each function in file
    for func in functions:
        code = filterBlockCode(getAsmFunctionBlock(text, func))
        size = len(code)
        for line in code:
            data = line.split()
            instruction = data[8].lower()
            # test if it's something we're looking for.
            if instruction in floatInstructions:
                # add it to dictionary
                if func not in lookup[instruction]:
                    lookup[instruction][func] = size
                    #print(func, size)


for instr in floatInstructions:
    limit = 50
    funcs = getShortestFuncs(lookup, instr, limit)
    label = instr + " "
    if len(funcs) >= limit:
        label += "(first " + str(limit) + " functions)"
    else:
        label += "(only " + str(len(funcs)) + " functions)"

    print(label)
    print("=" * len(label))
    for f in funcs:
        print(lookup[instr][f], f.replace(":", ""))
    print()
