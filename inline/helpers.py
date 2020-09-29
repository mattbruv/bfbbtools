import re
from sanitize import desanitize
from files import getAsmFiles

labelRegex = r".+:"

def getLabels(fileText, strip=False):
    matches = re.findall(labelRegex, fileText)
    if strip:
        matches = list(map(lambda x: x.replace(":", ""), matches))
    return matches

def getAsmFunctions(fileText, strip=False):
    matches = getLabels(fileText, strip)
    return list(filter(lambda x: "lbl_" not in x, matches))

def getAsmFunctionBlock(fileText, label):
    data = []
    found = False
    for line in fileText.splitlines():
        if label in line:
            found = True
            continue
        if found:
            data.append(line.strip())
            if len(line) == 0:
                break
    return data

def getBlockLabels(block):
    labels = set()
    for line in block:
        for label in extractLabels(line):
            labels.add(label)
    return labels

def getBlockFunctionCalls(block):
    labels = set()
    for line in block:
        for label in extractFunctionCalls(line):
            labels.add(label)
    return labels


labelRegexes = [
    r"\bb.+ (.+)$", # after branch instructions
    r"\ (\D\S+)@(ha|l)$", # before @ha, @l
    r"(\w+)-_" # before -SDA
]

def extractFunctionCalls(line):
    labels = set()
    matches = re.findall(labelRegexes[0], line)
    for m in matches:
        if type(m) != str:
            labels.add(m[0])
        else:
            labels.add(m)
    return labels

def extractLabels(line):
    labels = set()
    for r in labelRegexes:
        matches = re.findall(r, line)
        for m in matches:
            if type(m) != str:
                labels.add(m[0])
            else:
                labels.add(m)
    return labels

def externBlock(lines):
    block = """extern "C" {
    {lines}
}
""".replace("{lines}", "\n    ".join(lines))
    return block

def funcString(funcName):
    return "extern void " + funcName + "();"

def labelString(labelName):
    return "extern int " + labelName + ";"

def blockToCPP(name, block):
    name = name.replace(":", "")
    code = "asm void " + name + "()\n{\n"
    code += "    nofralloc\n"
    for b in block:
        b = b.strip()
        if "/*" in b:
            code += "    " + b.split("\t")[1] + "\n"
        elif b != "":
            code += b + "\n"
    code += "}\n"
    return code

def getSource(name):
    files = list(filter(lambda x: name.lower() in x.name.lower(), getAsmFiles()))
    if len(files) > 1:
        print("Error: Ambiguous filename:", name)
        print("Please specify filename in greater detail.")
        for f in files:
            print(f)
        quit()
    if len(files) == 0:
        print("Error: No files including", name)
        quit()
    return files[0]


def filterBlockCode(block):
    return list(filter(lambda x: "/*" in x, block))

def codeLineToBytes(line):
    d = line.split()
    b = "0x" + "".join(d[3:7])
    return b

def blockToBytes(block):
    code = filterBlockCode(block)
    return list(map(codeLineToBytes, code))

funcTemplate = """asm void {name}() {
    nofralloc
    {data}
}"""

def writeFunctions(source, funcList):
    source += """extern "C" {\n"""
    for f in funcList:
        source += "    void " + f + "();\n"
    source += "}\n"
    return source

def bytesToString(byteLine):
    return "opword" + " " + byteLine

def writeCode(source, funcName, byteLines):
    source += "\n"
    t = funcTemplate.replace("{name}", funcName)
    bs = list(map(bytesToString, byteLines))
    t = t.replace("{data}", "\n    ".join(bs))
    source += t + "\n"

    return source