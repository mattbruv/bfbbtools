
substitutions = (
    ('<',  '$$0'),
    ('>',  '$$1'),
    ('@',  '$$2'),
    ('\\', '$$3'),
    (',',  '$$4'),
    ('-',  '$$5')
)

def desanitize(string):
    for s in substitutions:
        string = string.replace(s[1], s[0])
    return string

def newSanitize(string):
    for s in substitutions:
        string = string.replace(s[0], s[1])
    return string