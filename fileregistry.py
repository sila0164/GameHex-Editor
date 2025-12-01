import db

def filechecker(intread):
    print(f"Filecheck:")
    filename = None
    filetype = None
    for fn, value in db.weapondbentries.items():
        if value == intread:
            filename = fn
            filetype = "WeaponDB"
            break
    for fn, value in db.muzzledbentries.items():
        if value == intread:
            filename = fn
            filetype = "MuzzleDB"
            break
    print(f"Filename: {filename}\nFile type: {filetype}\n\n----------------------------------------------------------------------------\n\n")
    return filename, filetype 
        
def scriptrunner(filetype):
    if filetype == "WeaponDB":
        from scripts.WeaponDB import WeaponDB
        WeaponDB()
    elif filetype == "MuzzleDB":
        from scripts.MuzzleDB import MuzzleDB
        MuzzleDB()
    else:
        print("CRITICAL: Scriptrunner found no script to run from filetype....")