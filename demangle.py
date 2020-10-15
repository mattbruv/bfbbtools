import subprocess
import re

asmTemplate = """
    .section .text
    .global {func}
    {func}:
        bl {func}
"""

regex = re.compile(r"multiply-defined:\s'(.*)'\sin\s", re.DOTALL)

ass = ["../bfbbdecomp/tools/mwcc_compiler/2.7/mwasmeppc.exe"]
ld = ["../bfbbdecomp/tools/mwcc_compiler/2.7/mwldeppc.exe"]

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
    print()
    print("DEMANGLE:", functionName)
    asm = asmTemplate.replace("{func}", functionName)
    open("test1.s", "w").write(asm)
    open("test2.s", "w").write(asm)
    subprocess.run(ass + ["test1.s"])
    subprocess.run(ass + ["test2.s"])
    process = subprocess.Popen(ld + ["test1.o", "test2.o"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    output = out.decode("utf-8")
    name = regex.findall(output)[0]
    name = defuckify(name)
    return name
