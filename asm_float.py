from asm import getSections
from pathlib import Path
import struct

asmPath = Path("../bfbbdecomp/asm/Game/zNPCTypeBossSandy.s")

asmSource = open(asmPath).read()

sections = getSections(asmSource)

sdata2 = sections[".sdata2"]

symbol = None

rom = open("../bfbbdecomp/baserom.dol", "rb")

label = None

floats = []

for line in sdata2:
    if ":" in line:
        data = line.split(":")
        label = data[0]
    if ".incbin" in line:
        data = line.split()
        start = int(data[2].replace(",", ""), 16)
        rom.seek(start)
        byteData = rom.read(4)
        floatHex = struct.unpack(">I", byteData)[0]
        #print(floatHex)
        floatData = struct.unpack(">f", byteData)[0]
        #print(floatData, hex(floatHex))
        floats.append([label, floatData, hex(floatHex)])

print(floats)
cppPath = "../bfbbdecomp/src/Game/zNPCTypeBossSandy.cpp"
cppSource = open(cppPath).read()

cpp = "\n".join(
    list(
        map(
            lambda x: "extern float32 " + x[0] + "; // " + str(x[1]) + "   " +
            x[2].replace("0x", ""), floats)))

print(cpp)

cppSource = cppSource.replace("// FLOATS", cpp)
open(cppPath, "w").write(cppSource)

for f in floats:
    lbl = f[0] + ":"
    asmSource = asmSource.replace(lbl, ".global " + f[0] + "\n" + lbl)
open(asmPath, "w").write(asmSource)