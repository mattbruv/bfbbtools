# __vt__10zNPCBSandy:
# .incbin "baserom.dol", 0x296CAC, 0xDC
import subprocess

from symbols import getSymbols


def processTableBytes(data):
    l = list(data)
    l = list(map(lambda x: hex(x)[2:].zfill(2), l))
    addrs = []
    i = 1
    s = ""
    for byte in l:
        s += byte
        i += 1
        if i == 5:
            addrs.append(s)
            s = ""
            i = 1
    return addrs


def readVTable(start, length):
    print(start, length, "size =", length // 4)
    file = open("../bfbbdecomp/baserom.dol", "rb")
    file.seek(start)
    info = file.read(length)
    return processTableBytes(info)


syms = getSymbols()
funcDict = {}
for s in syms:
    if s["type"] == "FUNC":
        funcDict[s["address"]] = s["name"]


def getFuncName(addr):
    if addr.upper() in funcDict:
        return funcDict[addr.upper()]
    return "NULL"


def filt(name):
    return subprocess.check_output(["c++filt.exe", name]).decode().strip()


info = readVTable(0x296cac, 0xdc)
table = list(map(getFuncName, info))
table = list(map(filt, table))

code = "/*\n"
i = 0
for t in table:
    s = "    " + str(i) + " " + str(hex(
        i * 4)) + " " + info[i] + " " + t + "\n"
    code += s
    print(s)
    i += 1
code += "*/"

path = "../bfbbdecomp/src/Game/zNPCTypeBossSandy.h"
text = open(path, "r").read()
text = text.replace("// VTABLE", code)
open(path, "w").write(text)