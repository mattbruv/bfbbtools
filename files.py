from pathlib import Path
from path import *

def getAsmFiles():
    return list(Path(pathASM).rglob("*.s"))
