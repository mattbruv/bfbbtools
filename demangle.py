import subprocess
import re

asmTemplate = """
    .section .text
    .global {func}
    {func}:
        bl {func}
"""

regex = re.compile(r"multiply-defined:\s'(.*)'(?:.*?)\sin\s", re.DOTALL)

ass = ["../bfbbdecomp/tools/mwcc_compiler/2.7/mwasmeppc.exe"]
ld = ["../bfbbdecomp/tools/mwcc_compiler/2.7/mwldeppc.exe"]

subTypes = [
    ("char", "int8"),
    ("short", "int16"),
    ("int", "int32"),
    ("long long", "int64"),
    ("unsigned char", "uint8"),
    ("unsigned short", "uint16"),
    ("unsigned int", "uint32"),
    ("unsigned long long", "uint64"),
    ("float", "float32"),
    ("double", "float64"),
    ("long", "long32"),
    ("unsigned long", "ulong32"),
]

subTypes.sort(key=lambda x: -len(x[0]))

def defuckify(name):
    lines = name.splitlines()
    data = []
    for l in lines:
        while l[0] == '#':
            l = l.replace('#', '', 1)
        res = l.strip()
        data.append(res)
    res = " ".join(data).strip()
    #res = res.replace(",", ", ")
    return res

def demangleFunction(functionName):
    #print()
    #print("DEMANGLE:", functionName)
    asm = asmTemplate.replace("{func}", functionName)
    open("test1.s", "w").write(asm)
    open("test2.s", "w").write(asm)
    subprocess.run(ass + ["test1.s"])
    subprocess.run(ass + ["test2.s"])
    process = subprocess.Popen(ld + ["test1.o", "test2.o"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    output = out.decode("utf-8")
    name = regex.findall(output)
    if len(name) == 0:
        return None
    name = defuckify(name[0])
    return name

#print(demangleFunction("xAnimTableAddFile__FP10xAnimTableP9xAnimFilePCc"))