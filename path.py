
path = "../bfbbdecomp/"
pathASM = path + "asm/"

def asmToSrcPath(asmPath):
    path = asmPath.replace("\\asm\\", "\\src\\")
    path = path.replace(".s", ".cpp")
    return path