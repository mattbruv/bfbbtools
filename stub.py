from parseasm import parseAsm
from symbols import getSymbols
import re

# zNPCTypeBossSandy.cpp


def isCodeLine(line):
    data = line.split(" ")
    if len(data) < 2:
        return False
    addr = data[1]
    if not re.match(r"([0-9a-fA-F]{8})", addr):
        return False
    return True


def getAddress(line):
    return line.split(" ")[1]


def firstAddress(lines):
    line = next(filter(isCodeLine, lines))
    return getAddress(line)


def lastAddress(lines):
    line = next(reversed(list(filter(isCodeLine, lines))))
    return getAddress(line)


def symbolBetween(symbol, first, last):
    if symbol["type"] != "FUNC":
        return False
    addr = int(symbol["address"], 16)
    return addr >= int(first, 16) and addr <= int(last, 16)


def getFunctionsBetween(first, last):
    syms = getSymbols()
    funcs = list(filter(lambda x: symbolBetween(x, first, last), syms))
    funcs.sort(key=lambda x: int(x["address"], 16))
    return funcs


def getAllAsmFunctions(lines):
    first = firstAddress(lines)
    last = lastAddress(lines)
    funcs = getFunctionsBetween(first, last)
    return funcs


def getAddressLabel(lines, address):
    name = None
    found = False
    for line in reversed(lines):
        if not found:
            if "/* " + address in line:
                found = True
            continue
        if isCodeLine(line):
            break
        if ":" in line:
            return line.replace(":", "")
    return name


def fixAssembly(path):
    asmText = open(path).read()
    blocks = parseAsm(path)
    textBlock = blocks[".text"]
    lines = textBlock.splitlines()
    funcs = getAllAsmFunctions(lines)
    i = 0
    for f in funcs:
        lbl = getAddressLabel(lines, f["address"])
        print(f["address"], lbl, f["name"])
    print(i)


def run():
    fixAssembly("../bfbbdecomp/asm/Game/zNPCTypeBossSandy.s")


run()
