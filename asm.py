import re

sectionRegex = r".section\s+(\S*)\s?"


def getSections(asmText):
    sections = {}
    current = None
    for line in asmText.splitlines():
        match = re.match(sectionRegex, line)
        if match:
            current = match[1]
            sections[current] = []
        if current:
            sections[current].append(line)
    return sections