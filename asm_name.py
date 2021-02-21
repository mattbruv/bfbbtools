from pathlib import Path
from symbols import getSymbols
from files import getAsmFiles
import re

lblRegex = r"lbl_([0-9a-fA-F]+):"


def isSymbol(addr):
    for s in symbols:
        if s["address"] == addr:
            if s["type"] == "SECTION":
                continue
            return s
    return None


asmPath = Path("../bfbbdecomp/asm/Game/zNPCTypeBossSandy.s")
source = open(asmPath).read()
symbols = getSymbols()

matches = re.findall(lblRegex, source)

for match in matches:
    sym = isSymbol(match)
    if not sym:
        continue
    if sym["scope"] != "LOCAL":
        print("NOT LOCAL", sym)
        continue
    if not sym["name"]:
        continue

    name = sym["name"].replace("@", "_")
    print(sym, name)
    source = source.replace("lbl_" + match, name)
open(asmPath, "w", newline="").write(source)