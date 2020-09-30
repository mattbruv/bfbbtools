import glob
from pathlib import Path
from symbols import getSymbols
import json

typeMap = {}

syms = list(filter(lambda x: x["name"] != None and x["type"] == "FUNC" and x["scope"] == "GLOBAL", getSymbols()))

def getType(lines, name):
    found = 0
    for l in lines:
        if name in l and found == 0:
            found = 1
        if found:
            found += 1
            if found == 3 and "Start address" not in l:
                break
            if found > 3:
                return l.strip()
    return name

typeDict = {}

for cpp in Path('types').rglob('*.cpp'):
    data = open(cpp).read()
    lines = open(cpp).readlines()
    print(cpp)

    for s in syms:
        n = s["name"]
        if n in data:
            valtype = getType(lines, n)
            if n not in typeDict:
                if valtype != n:
                    typeDict[n] = valtype
                else:
                    print(n, "==", valtype)

open("types.json", "w").write(json.dumps(typeDict, sort_keys=True, indent=4, separators=(',', ': ')))
    


