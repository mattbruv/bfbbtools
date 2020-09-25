from symbols import *
from files import *

substitutions = (
    ('<',  '$$0'),
    ('>',  '$$1'),
    ('@',  '$$2'),
    ('\\', '$$3'),
    (',',  '$$4'),
    ('-',  '$$5')
)

def newSanitize(string):
    for s in substitutions:
        string = string.replace(s[0], s[1])
    return string

symbols = getSymbols()
asm = getAsmFiles()

def patch(syms):
    for path in asm:
        print(path)
        data = open(path, newline="").read()
        for symbol in syms:
            old = sanitize(symbol["name"])
            new = newSanitize(symbol["name"])
            data = data.replace(old, new)
        open(path, 'w', newline="").write(data)

bad = list(filter(lambda x: x["scope"] == "LOCAL" and x["type"] == "FUNC" and x["name"] is not None and not isValidName(x["name"]), symbols))
patch(bad)

bad = list(filter(lambda x: x["scope"] == "GLOBAL" and x["type"] == "FUNC" and x["name"] is not None and not isValidName(x["name"]), symbols))
patch(bad)

bad = list(filter(lambda x: x["scope"] == "GLOBAL" and x["type"] == "OBJECT" and x["name"] is not None and not isValidName(x["name"]), symbols))
patch(bad)