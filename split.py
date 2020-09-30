from files import getAsmFiles
from parseasm import *
import os


def separateAsm(filepath):
    sections = parseAsm(filepath)
    out = str(filepath).replace("\\asm\\", "\\data\\")
    text = open(filepath).read()
    print(out)
    for s in sections:
        if s != ".text":
            text = text.replace(sections[s], "")
    open(filepath, "w").write(text.strip() + "\n")
    f = open(out, "w+")
    for s in sections:
        if s != ".text":
            f.write(sections[s].strip() + "\n")
    f.close()

for asm in getAsmFiles():
    path = str(asm)
    if "Core" not in path and "Game" not in path:
        continue
    separateAsm(path)


