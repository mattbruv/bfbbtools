from symbols import getSymbols
from files import getAsmFiles
from sanitize import sanitizeLabel, desanitizeLabel
import re


def isGameCode(symbol):
    addr = int(symbol["address"], 16)
    inBounds = addr >= 0x800058E0 and addr <= 0x8019687C
    return inBounds and symbol["type"] == "FUNC"


def getAsm():
    asmFiles = getAsmFiles()
    asm = []
    for f in asmFiles:
        asm.append({"name": f.name, "path": f, "text": open(f).read()})
    return asm


def getCodeLine(addr, text):
    search = "(\/\* {}.+\n)".format(addr)
    match = re.findall(search, text)
    return match[0]


def cleanFile(asm, symbols, name):
    data = next(x for x in asm if x["name"] == name)
    text = data["text"]

    for sym in symbols:
        n = sym["name"]
        # n = #sanitizeLabel(n)
        addr = sym["address"]
        start = int(addr, 16)
        size = sym["size"]
        end = start + size - 4
        endAddr = "{:x}".format(end).upper()
        endAddr = endAddr.rjust(8, "0")
        scope = sym["scope"].lower()
        if n + ":" in text:
            text = text.replace(".global " + n, "")

            begin = ".fn " + n + ", " + scope
            endText = ".endfn " + n + "\n"
            text = text.replace(n + ":", begin)
            endLine = getCodeLine(endAddr, text)
            text = text.replace(endLine, endLine + endText)
            #print(n, addr, size, endAddr, endLine)

    open(data["path"], "w+", newline="\n").write(text)


symbols = list(filter(isGameCode, getSymbols()))
asm = getAsm()

cleanFile(asm, symbols, "zGameExtras.s")
