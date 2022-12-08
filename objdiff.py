from symbols import getSymbols
from files import getAsmFiles
from sanitize import sanitizeLabel, desanitizeLabel
import re
import subprocess


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

    # sort from longest to shortest
    # because some names overlap
    symbols = sorted(symbols, key=lambda s: len(s["name"]), reverse=True)

    for sym in symbols:
        n = sym["name"]
        realName = n
        n = sanitizeLabel(n)
        addr = sym["address"]
        start = int(addr, 16)
        size = sym["size"]
        end = start + size - 4
        endAddr = "{:x}".format(end).upper()
        endAddr = endAddr.rjust(8, "0")
        scope = sym["scope"].lower()

        local = "l_" + sym["address"][-4::].lower() + "_"

        for n in [local + n, n]:
            print(n)
            Found = False
            if n + ":" in text:
                print("found", n)
                Found = True

                unmangled = ""

                try:
                    unmangled = subprocess.check_output(
                        ["../bfbb/cwdemangle-windows-x86_64.exe",
                         realName]).decode("utf-8").strip()
                except:
                    pass

                text = text.replace(".global " + n, "")

                cppText = "/* cpp: " + unmangled + " */\n" if unmangled else ""

                begin = cppText + ".fn " + n + ", " + scope + ", " + str(
                    sym["size"]) + ""
                #endText = ".endfn " + n + "\n"
                text = text.replace(n + ":", begin)
                """
                try:
                    endLine = getCodeLine(endAddr, text)
                    text = text.replace(endLine, endLine + endText)
                except:
                    pass
                """
                #print(n, addr, size, endAddr, endLine)
            if Found:
                break

    open(data["path"], "w+", newline="\n").write(text)


symbols = list(filter(isGameCode, getSymbols()))
asm = getAsm()
"""
for f in asm:
    print(f["name"])
    cleanFile(asm, symbols, f["name"])
"""

cleanFile(asm, symbols, "zNPCTypeBossSandy.s")