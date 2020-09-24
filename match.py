import re

def matchFuncs(string):
    return set(re.findall(r"func_([0-9a-zA-Z]+)", string))

def matchLabels(string):
    return set(re.findall(r"lbl_([0-9a-zA-Z]+)", string))