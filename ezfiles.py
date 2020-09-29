from files import getAsmFiles

fs = getAsmFiles()
fs = sorted(fs, key=lambda x: -len(open(x).readlines()))

for f in fs:
    print(f, len(open(f).readlines()))