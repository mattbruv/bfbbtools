
path = "../bfbbdecomp/"
pathASM = path + "asm/"
pathCPP = path + "src/"

def asmToSrcPath(asmPath):
    path = asmPath.replace("\\asm\\", "\\src\\")
    path = path.replace(".s", ".cpp")
    return path