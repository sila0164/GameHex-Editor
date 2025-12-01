from func import statset, typesearch, typeread
from gui import mainwindow, mainwindowreset, topseparatorinit, bottomseparatorinit, extraseperator, filedisplayinit, filedisplay, createtabgroup, createtab, creategroup, createdropdown, createinputbox, createstatlist, createcheckbox
import func
import db

def muzzledbread():
    func.offset = 0
    typesearch("Start of modifiers", 1068465826, "u32", 1)
    statset(4, "modifieramount", "u8")
    if func.stattemp["modifieramount"]["value"] == 0:
        print("No modifiers found 1st run.")
        typesearch("Start of modifiers", 1068465826, "u32", 1)
        statset(4, "modifieramount", "u8")
        if func.stattemp["modifieramount"]["value"] == 0:
            print("No modifiers found 2nd run.")
            exit()
    for i in range(func.stattemp["modifieramount"]["value"]):
        func.offset += 48
        readname = typeread(func.offset, "u64")
        print(readname)
        nameoffset = func.offset
        try:
            for f, n in db.modifiernames.items():
                if n == readname:
                    name = f
                    break
            print(name)
        except:
            print(f"Unknown modifier {i}")
            name = "Unknown"
        func.stattemp[f"{name}add"] = {}
        func.stattemp[f"{name}mul"] = {}
        func.offset += 28
        func.stattemp[f"{name}add"]["value"] = typeread(func.offset, "float")
        func.stattemp[f"{name}add"]["offset"] = func.offset
        func.stattemp[f"{name}add"]["newvalue"] = typeread(func.offset, "float")
        func.stattemp[f"{name}add"]["type"] = "float"
        func.offset += 24
        func.stattemp[f"{name}mul"]["value"] = typeread(func.offset, "float")
        func.stattemp[f"{name}mul"]["offset"] = func.offset
        func.stattemp[f"{name}mul"]["newvalue"] = typeread(func.offset, "float")
        func.stattemp[f"{name}mul"]["type"] = "float"

def muzzledbui():
    mainwindowreset()
    mainwindow(buttonstop=("open", "empty", "copyu64"), buttonsbottom=("applyallwayson", "empty", "close"))
    topseparatorinit()
    bottomseparatorinit()
    extraseperator(1, "S")
    filedisplayinit()
    filedisplay()

    #Parameters tab
    createtabgroup()
    createtab("Parameters")
    #1st group
    creategroup("Modifiers")
    for i, b in func.stattemp.items():
        createinputbox(i)

def MuzzleDB():
    func.statdict = db.modifiernames
    func.stattemp = {}
    muzzledbread()
    print("print \n\n", func.stattemp, "\n\n", func.statdict, "\n\n")
    muzzledbui()