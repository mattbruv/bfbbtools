

def sectionName(line):
    return line.split()[1]

def parseAsm(filepath):
    data = open(filepath).readlines()
    sections = {}
    name = None
    for line in data:
        if ".section" in line:
            name = sectionName(line)
            sections[name] = [line]
            continue
        if name != None:
            sections[name].append(line)
        #print(line)
    for s in sections:
        sections[s] = ''.join(sections[s])
    return sections