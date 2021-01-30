from symbols import getSymbols

asm = "../bfbbdecomp/asm/Game/zGameExtras.s"
syms = getSymbols()


def processFile(path):
    text = open(path).read()
    print(text)


processFile(asm)