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
startAt = 0x28C1E4

rom.seek(startAt)
at = 0x8028f204

source = ""

charmap = {
    "0x40000": "Y",
    "0x20000": "X",
    "0x0": "0",
}

for cheat in cheats:
    code = []
    print(hex(at), cheat)
    for i in range(0, 16):
        data = rom.read(4)
        at += 4
        button = int.from_bytes(data, byteorder="big")
        code.append(button)
    print(cheat, code)
    source += "static uint32 " + cheat + "[16] = {"
    source += "\n"
    c = ','.join(map(lambda x: charmap[hex(x)], code))
    source += c
    source += "\n"
    source += "};"
    source += "\n"

cpp = "../bfbbdecomp/src/Game/zGameExtras.cpp"
text = open(cpp, "r").read()

text = text.replace("// REPLACE ME", source)
open(cpp, "w").write(text)