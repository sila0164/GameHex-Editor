from func import statset, typesearch, dicttypesearch
from gui import mainwindow, mainwindowreset, topseparatorinit, bottomseparatorinit, extraseperator, filedisplayinit, filedisplay, createtabgroup, createtab, creategroup, createdropdown, createinputbox, createstatlist, createcheckbox
import func
import db

#initial fileread (finds all needed values)
def weapondbread():
    
    #setup

    u8 = "u8"
    u16 = "u16"
    u32 = "u32"
    u64 = "u64"
    float = "float"

    func.offset = 14

    #Initial values
    statset(0, "rateoffire", u16)
    statset(42, "projectilebreakingangle", float)

    #Initloadtype search
    print("\nINITLOAD_TYPE\n")
    typesearch("Zero and Range", 1684107084, u32, 1)
    
    #Range
    if func.fileu64 in (1838530271017, 1838530266984):
        statset(145, "zero", float)
        statset(144, "range", float)
    else:
        statset(25, "zero", float)
        statset(24, "range", float)

    #Damage and penetration search
    print("\nDAMAGE\n")
    if func.fileu64 in (1698309626211, 1923391143335, 1698309626316):
        func.offset -= 8
    elif "Maxim9" in func.filename:
        typesearch("Damage and penetration", (1573516640874,), u64, 1)
    elif "MK23" in func.filename:
        typesearch("Damage and penetration", (1700302930594,), u64, 1)
    else:
        typesearch("Damage and penetration", (1921650116144,), u64, 1)
    
    statset(32, "damage", u16)
    statset(24, "penetration1", float)
    statset(4, "penetration2", float)

    #UI Grid search  
    print("\nUI GRID\n")
    # Handgun exception
    if "HDG" in func.filename or func.fileu64 in (1923391138966, 395649524046, 1698309626316, 1698309626211, 1923391143335, 1923391202491, 1956585197193):
        func.offset -= 8
    else:
        typesearch("UI Grid", (1573516640874, 1700302930594, 1297217990701), u64, 1)
    if func.fileu64 in (1838530271017, 1838530270468, 1838530266890, 205425832666): # A few files had two of the above before the grid.
        func.offset += 1
        typesearch("UI Grid", (1573516640874, 1700302930594), u64, 1)

    
    if "HDG" in func.filename or func.fileu64 in (1698309626211, 1698309626316, 1923391202491, 1956585197193, 1923391143335): # Incosistent values in some files. Some files didnt have the second velocity variable. All Handguns too fml....
        statset(32, "velocity2", float)
    else:
        statset(28, "velocity1", float)
        statset(4, "velocity2", float) 
    statset(4, "recoilpivot", float)
    if func.fileu64 in (1698309626211, 1698309626316): # These had a completely different ui grid order
        statset(4, "ui_noise", float) 
        statset(4, "ui_accuracy", float) 
    else:
        statset(8, "ui_accuracy", float) 
    statset(4, "ui_control", float) 
    statset(4, "ui_range", float) 
    statset(4, "ui_rateoffire", float)
    statset(4, "ui_unknown1", float)
    statset(4, "ui_unknown2", float) 
    statset(4, "ui_weight", float)
    if func.fileu64 in (1698309626211, 1698309626316):  # These had a completely different ui grid order
        statset(12, "timetoaim", float)
    else:
        statset(4, "ui_noise", float)
        statset(8, "timetoaim", float)

    #Sway and spread grid search
    print("\nSWAY & SPREAD GRID\n")
    typesearch("Sway and Spread Grid", (513, 1025), u32, 1)

    statset(5, "burdenfactor", float)
    statset(4, "sway", float)
    statset(5, "modulatedspreadmax", float)
    statset(4, "modulatedspreadmin", float)
    statset(4, "modulatedspreadironsights", float)
    statset(5, "ironsightspreadmultiplier", float)
    statset(4, "otsspreadmultiplier", float)
    statset(4, "spreadradiusmin", float)
    statset(4, "spreadradiusmax", float)
    statset(4, "spreadtimetomin", float)
    statset(4, "spreadtimetomax", float)
    statset(6, "gaussironsight", u64)
    statset(10, "gaussinstinct", u64)
    statset(10, "gaussots", u64)

    #End grid search
    print("\nEND GRID x3\n")
    if func.fileu64 in (1923391220806, 1956585197213):
        typesearch("End Grid", 4787326405004230656, u64, 1)
        statset(47, "recoilpattern", u64)
    else:
        typesearch("End Grid", 2197962680, u64, 3)
        statset(15, "recoilpattern", u64)
    statset(79, "soundfile", u64)
    statset(45, "tacticalreloadthreshold", float)
    statset(6, "walkspeedmultiplier", float)
    statset(8, "mobility", float)
    statset(8, "adssensitivity", float)
    statset(21, "soundrange", float)

    #ammotype and attachment search
    print("\nATTACHMENT GRID\n")
    dicttypesearch("Ammotype", u64, db.ammotype, "id")
    #for ammoname, ammodata in db.ammotype.items():
    #    searchname = str(ammodata["id"])
    #    typesearch("Attachment Grid", searchname, u64, 1)   
    statset(0, "ammotype", u64)
    statset(9, "spreadpattern", u64)
    typesearch("reloadtime", 1176597217, u32, 1)
    statset(-22, "reloadtime", float)
    
    

    print(f"{func.stattemp}")
#UI of weapondbeditor
def weapondbui():
    mainwindowreset()
    mainwindow(buttonstop=("open", "empty", "copyu64"), buttonsbottom=("apply", "calculate", "close"))
    topseparatorinit()
    bottomseparatorinit()
    extraseperator(1, "S")
    filedisplayinit()
    filedisplay()

    #Parameters tab
    createtabgroup()
    createtab("Parameters")
    #1st group
    creategroup("Required Parameters")
    createdropdown("ammotype")
    createinputbox("Weight")

    #2nd group
    creategroup("Optional Parameters")
    createinputbox("rateoffire")
    createcheckbox("Bullpup")
    createcheckbox("Onehanded")
    createinputbox("reloadtime")
    createinputbox("ui_accuracy")
    createinputbox("ui_control")
    createdropdown("recoilpattern")
    createdropdown("spreadpattern")
    createdropdown("soundfile")
    createdropdown("gaussironsight")
    createdropdown("gaussinstinct")
    createdropdown("gaussots")

    #Stats Tab
    createtab("Stats")
    creategroup("Primary Stats")
    createstatlist(stats=("rateoffire", "zero", "range", "damage", "penetration1", "penetration2", "velocity2", "reloadtime", "timetoaim", "burdenfactor", "mobility", "soundrange"))
    creategroup("UI Stats")
    createstatlist(stats=("ui_accuracy", "ui_control", "ui_range", "ui_weight", "ui_noise", "ui_rateoffire"))
    
    #Aux Stats Tab
    createtab("Aux Stats")
    creategroup("Spread")
    createstatlist(stats=("sway", "modulatedspreadmax", "modulatedspreadmin", "modulatedspreadironsights", "ironsightspreadmultiplier", "otsspreadmultiplier", "spreadradiusmin", "spreadradiusmax", "spreadtimetomin", "spreadtimetomax"))
    creategroup("Other")
    if "HDG" in func.filename or func.fileu64 in (1698309626211, 1698309626316, 1923391202491, 1956585197193, 1923391143335):  #Some files didnt have the second velocity variable.
        createstatlist(stats=("projectilebreakingangle", "recoilpivot", "ui_unknown1", "ui_unknown2", "tacticalreloadthreshold", "walkspeedmultiplier", "adssensitivity"))
    else:
        createstatlist(stats=("projectilebreakingangle", "velocity1", "recoilpivot", "ui_unknown1", "ui_unknown2", "tacticalreloadthreshold", "walkspeedmultiplier", "adssensitivity"))
   
def WeaponDB():
    func.statdict = {
    "rateoffire": "Rate Of Fire",
    "projectilebreakingangle": "ProjectileBreakingAngle",
    "zero": "Zero",
    "range": "Range",
    "damage": "Damage",
    "penetration1": "Penetration",
    "penetration2": "Penetration Ratio",
    "velocity1": "Muzzle Velocity",
    "velocity2": "Muzzle Velocity",
    "recoilpivot": "Recoil Pivot",
    "ui_accuracy": "Accuracy",
    "ui_control": "Control",
    "ui_range": "Range",
    "ui_rateoffire": "Rate Of Fire",
    "ui_unknown1": "Unknown UI Float",
    "ui_unknown2": "Unknown UI Float",
    "ui_weight": "Weight",
    "ui_noise": "Noise",
    "timetoaim": "Time To Aim",
    "burdenfactor": "Sway",
    "sway": '"Sway"',
    "modulatedspreadmax": "Modulated Spread Max",
    "modulatedspreadmin": "Modulated Spread Min",
    "modulatedspreadironsights": "Modulated Spread Ironsights",
    "ironsightspreadmultiplier": "Ironsight Spread Multiplier",
    "otsspreadmultiplier": "OTS Spread Multiplier",
    "spreadradiusmin": "Spread Radius Min",
    "spreadradiusmax": "Spread Radius Max",
    "spreadtimetomin": "Spread Time to Min",
    "spreadtimetomax": "Spread Time to Max",
    "gaussironsight": "Gauss Ironsight",
    "gaussinstinct": "Gauss Instinct",
    "gaussots": "Gauss OTS",
    "recoilpattern": "Recoil Pattern",
    "soundfile": "Sound File",
    "tacticalreloadthreshold": "Tactical Reload Threshold",
    "walkspeedmultiplier": "Walk Speed Multiplier",
    "mobility": "Mobility",
    "adssensitivity": "ADS Sensitivity",
    "soundrange": "Sound Range",
    "bulletdb": "Bullet DB",
    "reloadtime": "Reload Time",
    "ammotype": "Ammo Type",
    "spreadpattern": "Spread Pattern",
}
    weapondbread()
    weapondbui()
    



