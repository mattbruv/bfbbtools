from parseasm import parseAsm
from symbols import getSymbols
import re
from pathlib import Path
import subprocess
from files import getAsmFiles
from sanitize import sanitizeLabel, desanitizeLabel

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


def getFullLine(lines, search):
    for line in lines:
        if search in line:
            return line
    return None


def fixAssembly(path):
    asmText = open(path).read()
    blocks = parseAsm(path)
    if ".text" not in blocks:
        return
    textBlock = blocks[".text"]
    newBlock = blocks[".text"]
    lines = textBlock.splitlines()
    funcs = getAllAsmFunctions(lines)

    for f in funcs:
        funcName = sanitizeLabel(f["name"])
        if f["address"] not in textBlock:
            print("Already Decompiled", funcName)
            continue
        lbl = getAddressLabel(lines, f["address"])
        if lbl != None and lbl == funcName:
            continue
        print(f["address"], f["scope"], lbl, funcName)
        if lbl == None:
            line = getFullLine(lines, "/* " + f["address"])
            newLabel = "\n" + funcName + ":\n"
            newBlock = newBlock.replace(line, newLabel + line)
            print(line)
            pass
        else:
            line = getFullLine(lines, lbl + ":")
            newBlock = newBlock.replace(line, "\n" + line)
            newBlock = newBlock.replace(lbl, funcName)
            pass
    asmText = asmText.replace(textBlock, newBlock)
    open(path, "w").write(asmText)


def run():
    asms = getAsmFiles()
    path = Path("../bfbbdecomp/asm/Game/zNPCTypeBossPlankton.s")
    fixAssembly(path)
    subprocess.run(["python", "inlineasm.py", path.name])


run()
