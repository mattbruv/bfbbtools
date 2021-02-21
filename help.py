import struct

cheats = [
    "sCheatAddShiny",
    "sCheatAddSpatulas",
    "sCheatBubbleBowl",
    "sCheatCruiseBubble",
    "sCheatMonsterGallery",
    "sCheatArtTheatre",
    "sCheatChaChing",
    "sCheatExpertMode",
    "sCheatSwapCCLR",
    "sCheatSwapCCUD",
    "sCheatRestoreHealth",
    "sCheatShrapBob",
    "sCheatNoPants",
    "sCheatCruiseControl",
    "sCheatBigPlank",
    "sCheatSmallPeep",
    "sCheatSmallCoStars",
    "sCheatRichPeep",
    "sCheatPanHandle",
    "sCheatMedics",
    "sCheatDogTrix",
    #"sCheatPressed",
]

rom = open("../bfbbdecomp/baserom.dol", "rb")
startAt = 0x28C724

rom.seek(startAt)

source = ""

for cheat in cheats:
    print(cheat)
    key_code = struct.unpack(">I", rom.read(4))[0]
    callback = struct.unpack(">I", rom.read(4))[0]
    flg_keep = struct.unpack(">I", rom.read(4))[0]
    flg_mode = struct.unpack(">I", rom.read(4))[0]
    print(hex(key_code), hex(callback), hex(flg_keep), hex(flg_mode))
    source += "{"
    source += cheat + ", "
    source += "NULL, "
    source += hex(flg_keep) + ", "
    source += str(flg_mode) + "}, "
    source += "// " + hex(callback) + "\n"

cpp = "../bfbbdecomp/src/Game/zGameExtras.cpp"
text = open(cpp, "r").read()

text = text.replace("// CHEATLIST", source)
open(cpp, "w").write(text)