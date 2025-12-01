import os
import webbrowser
import struct
from tkinter import *
from tkinter import ttk
import db
from tkinter import filedialog
from fileregistry import filechecker, scriptrunner
import func


#Search/Read functions
def multistatset(addtooffset, name, type, amountvar, offsetbetween):
    global offset
    global stattemp
    offset += addtooffset
    amountvar = func.stattemp[amountvar]["value"]
    print(f"Setting {name} @ {offset + addtooffset} as {type}")
    for i in range(amountvar):
        value = typeread(offset, type)
        vardictname = f"{name}{i}"
        vardict = {}
        vardict["value"] = value
        vardict["refname"] = "Unknown"
        if name == "ammotype":
            print("Ammo Type Detected")
            vardict["newvalue"] = value
            for refname, r in getattr(db, name).items():
                if isinstance(r, dict) and r.get("id") == value:
                    vardict["refname"] = refname
                    print(f"Set as {vardict["refname"]}")
                    break
        elif type == "u64":
            print("Reference Detected")
            vardict["newvalue"] = value
            for refname, r in getattr(db, name).items():
                if r == value:
                    vardict["refname"] = refname
                    print(f"Set as {vardict["refname"]}")
                    break
        else:
            vardict["newvalue"] = "Not Set"
        vardict["offset"] = offset
        vardict["type"] = type
        stattemp[vardictname] = vardict
        if amountvar != 0:
            offset += offsetbetween
def statset(addtooffset, name, type):
    global offset
    global stattemp
    print(f"Setting {name} @ {offset + addtooffset} as {type}")
    offset += addtooffset
    value = typeread(offset, type)
    vardict = {}
    vardict["value"] = value
    vardict["refname"] = "Unknown"
    if name == "ammotype":
        print("Ammo Type Detected")
        vardict["newvalue"] = value
        for refname, r in getattr(db, name).items():
            if isinstance(r, dict) and r.get("id") == value:
                vardict["refname"] = refname
                print(f"Set as {vardict["refname"]}")
                break
    elif type == "u64":
        print(f"Reference Detected: {value}")
        vardict["newvalue"] = value
        for refname, r in getattr(db, name).items():
            if r == value:
                vardict["refname"] = refname
                print(f"Set as {vardict["refname"]}")
                break
    else:
        vardict["newvalue"] = "Not Set"
    vardict["offset"] = offset
    vardict["type"] = type
    stattemp[name] = vardict
def dicttypesearch(name, type, searchdict, subdict=None,):
    global offset
    print(f"Searching for{name} {type} from {offset}")
    startoffset = offset
    currentoffset = offset
    count = offset + 1000
    for i, dictname in searchdict.items():
        if subdict == None:
            searchstring = dictname
        else:
            searchstring = dictname[subdict]
        if not isinstance(searchstring, (tuple, list)):
            searchstring = (searchstring,)
        while True:
            search = typeread(currentoffset, type)
            if search in searchstring:
                print(f"Found {name} @ {offset}")
                offset = currentoffset
                return
            elif count == currentoffset:
                print(f"{searchstring} not found, limit has been reached.")
                currentoffset = startoffset
                break
            else:
                currentoffset += 1
    print(f"Failed to find {name}")
    messagewindow("warning", 
    f"Could not find: {name}",
    f"You can choose to ignore this warning, but results will not be correct for {name}.", 
    buttons=("ignore", "close", "report",))
def typesearch(name, searchstring, type, times):
    global offset
    print(f"Searching for {searchstring} as {type} from {offset}")
    count = offset + 1000
    fin = 0
    if not isinstance(searchstring, (tuple, list)):
        searchstring = (searchstring,)
    while fin != times: 
        search = typeread(offset, type)
        if search in searchstring:
            fin += 1
            print(f"Found {name} - {searchstring} @ {offset}")
            if fin != times:
                offset += 1
        elif count == offset:
            print(f"{searchstring} not found, limit has been reached.")
            offset = count - 1000
            messagewindow("warning", 
            f"Could not find: {name}",
            f"You can choose to ignore this warning, but results will not be correct for {name}.", 
            buttons=("ok", "close", "report",))
            return
        else:
            offset += 1
    if fin == 0:
        print(f"Failed to find {searchstring}")
        offset = count - 1000
        messagewindow("warning", 
        f"Could not find: {name}",
        f"You can choose to ignore this warning, but results will not be correct for {name}.", 
        buttons=("ignore", "close", "report",))
def typeread(offset, type):
    global filepath
    #print(f"running typeread @ {offset} as {type}")
    with open(filepath, "rb") as f:
        types = {
            "u8": 1,
            "u16": 2,
            "u32": 4,
            "u64": 8,
        }
        data = f.read()
        start = offset
        if type in types:
            typelength = types[type]
            #print(f"Data read as {types[type]} @ {offset}")
            end = offset + typelength
            filehex = data[start:end]
            read = int.from_bytes(filehex, byteorder="little")
        elif type == "float":
            #print(f"Data read as float @ {offset}")
            end = offset + 4
            filehex = data[start:end]
            read = struct.unpack('<f', filehex)[0]
        return read  

    try:
        if temp[f"{var_name}typ"] == "float":
            value = temp[var_name]
            return f"{value:.1f}"
        return temp[var_name]
    except KeyError:
        return "missing parameters"
#Write Function
def typewrite(offset, type_, value):
    global filepath

    # Samme byte-størrelser som i typeread
    types = {
        "u8": 1,
        "u16": 2,
        "u32": 4,
        "u64": 8,
    }

    # Åbn filen for både læs og skriv (binært)
    with open(filepath, "r+b") as f:
        f.seek(offset)

        if type_ in types:
            # Konverter integer til bytes i little-endian
            data = int(value).to_bytes(types[type_], byteorder="little")
            f.write(data)

        elif type_ == "float":
            # Pak float som little-endian float
            data = struct.pack("<f", float(value))
            f.write(data)

        else:
            raise ValueError(f"Ukendt type: {type_}")
def writestats():
    global stattemp
    for name, data in stattemp.items():
        newval = data.get("newvalue", None)
        if newval is not None and newval != "Not Set":
            offset = data["offset"]
            type_ = data["type"]
            print(f"Writing {name} ({type_}) @ {offset}: {data['value']} -> {newval}")
            typewrite(offset, type_, newval)
            data["value"] = newval
        else:
            print(f"Skipping {name}: newvalue not set")
    refreshstatvalue()
#Button functions
def terminateall():
    global root
    root.quit()
    root.destroy()    
def copyclipboard(string):
    global root
    print(f"Copying {string} to clipboard")
    root.clipboard_clear()        
    root.clipboard_append(string)  
    root.update()        
def copyfileu64():
    global fileu64
    copyclipboard(fileu64)
def report():
    global filename, projectfolder, errorfile
    print("Reporting bug")
    errorfilename = os.path.basename(errorfile) 
    logfile = os.path.join(projectfolder, "Log.txt")
    print(f"---------------------------------------------------------------------------------------\n\nOpen file:\n{errorfilename}", flush=True)
    with open(logfile, "r", encoding="utf-8") as f:
        out = f.read()
        copyclipboard(out)
    webbrowser.open("https://www.nexusmods.com/ghostreconbreakpoint/mods/1585?tab=bugs")
def openfile():
    global fileu64, filepath, statdict, stattemp, filename, inputboxes, filetype
    print("Opening file")
    if fileu64 and 'disabled' not in func.applybtn.state():
        messagewindow("info",
        "Warning",
        "If current settings have not been applied to the current file, they will not be recoverable.",
        buttons=("ok",),
        )
    tempfilepath = filedialog.askopenfilename(title="Open a File")
    if tempfilepath:
        print(f"Running filecheck on file")
        with open(tempfilepath, "rb") as f:
            data = f.read()
            filehex = data[1:9]
            intread = int.from_bytes(filehex, byteorder="little")
        selectedfilename = os.path.basename(tempfilepath)
        print(f"Selected filename: {selectedfilename}\nFile ID: {intread}")
        tempfilename, tempfiletype = filechecker(intread)
        if tempfilename == None:
            func.errorfile = tempfilepath
            messagewindow("warning", 
            "Unsupported File",
            "The selected file did not get recognized as a supported file by the program.", 
            buttons=("ok", "report"))
            return
        else:
            statdict = {}
            stattemp = {}
            inputboxes = {}
            fileu64 = intread
            filepath = tempfilepath
            filename = tempfilename
            filetype = tempfiletype
            scriptrunner(filetype)
def refreshstatvalue():
    for s in func.stattemp:
        stat = func.stattemp[s]
        labels = stat.get("labels")
        polished = stat.get("value")
        if labels:
            if isinstance(polished, float):
                polished = f"{polished:.2f}"
            labels["current"].config(text=polished)
def refreshstatnewvalue():
    for s in func.stattemp:
        stat = func.stattemp[s]
        labels = stat.get("labels")
        polished = stat.get("newvalue")
        if labels:
            if isinstance(polished, float):
                polished = f"{polished:.2f}"
            labels["new"].config(text=polished)
def calculate(): # Redo as functions for editor... Can be way simpler/more versatile
    
    #pull input
    print("Calculating stats")
    global Bullpup
    bullpup = Bullpup.get()
    global Onehanded
    onehanded = Onehanded.get()
    global inputboxes
    global stattemp
    try:
        weight = float(inputboxes["Weight"].get())
    except ValueError:
        messagewindow("info", "Weight is not a number", "Please make sure the value entered in the Weight box is a valid number.", buttons=("ok",))
        return
    try:
        rof = int(inputboxes["rateoffire"].get())
    except ValueError:
        rof = stattemp["rateoffire"]["value"]
    ammotyp = inputboxes["ammotype"].get()
    barrel = inputboxes["barrels"].get()
    accuracy = inputboxes["ui_accuracy"].get()
    control = inputboxes["ui_control"].get()
    print(f"Inputs: {ammotyp} {barrel} {rof} {weight} {bullpup} {onehanded}")

    #External Refs
    stattemp["ammotype"]["newvalue"] = db.ammotype[ammotyp]["id"]
    stattemp["gaussironsight"]["newvalue"] = db.gaussironsight[inputboxes["gaussironsight"].get()]
    stattemp["gaussinstinct"]["newvalue"] = db.gaussinstinct[inputboxes["gaussinstinct"].get()]
    stattemp["gaussots"]["newvalue"] = db.gaussots[inputboxes["gaussots"].get()]
    stattemp["recoilpattern"]["newvalue"] = db.recoilpattern[inputboxes["recoilpattern"].get()]
    stattemp["soundfile"]["newvalue"] = db.soundfile[inputboxes["soundfile"].get()]
    stattemp["spreadpattern"]["newvalue"] = db.spreadpattern[inputboxes["spreadpattern"].get()]
    print(f"External references set: ammotype: {stattemp["ammotype"]["newvalue"]} {db.ammotype[ammotyp]}")

    #1st data set (hard values from input)
    stattemp["rateoffire"]["newvalue"] = rof
    stattemp["damage"]["newvalue"] = db.ammotype[ammotyp]["damage"]
    stattemp["zero"]["newvalue"] = db.ammotype[ammotyp]["zero"]
    stattemp["range"]["newvalue"] = db.ammotype[ammotyp]["barrels"][barrel]["range"]
    if "HDG" not in func.filename and func.fileu64 not in (1698309626211, 1698309626316, 1923391202491, 1956585197193, 1923391143335):  #Some files didnt have the second velocity variable.
        stattemp["velocity1"]["newvalue"] = db.ammotype[ammotyp]["barrels"][barrel]["velocity"]
    stattemp["velocity2"]["newvalue"] = db.ammotype[ammotyp]["barrels"][barrel]["velocity"]
    stattemp["penetration1"]["newvalue"] = db.ammotype[ammotyp]["penetration1"]
    stattemp["penetration2"]["newvalue"] = db.ammotype[ammotyp]["penetration2"]
    stattemp["soundrange"]["newvalue"] = db.ammotype[ammotyp]["soundrange"]
    if bullpup == 1:
        factor = 0.3
    elif onehanded == 1:
        factor = 0.5
    else:
        factor = 1
    magazineweight = float(db.ammotype[ammotyp]["magweight"])
    magazineweightmod = magazineweight*factor
    print(f"Hard values set: ammoid: {stattemp["ammotype"]["newvalue"]}\n{ stattemp["rateoffire"]["newvalue"]} {stattemp["damage"]["newvalue"]} {stattemp["zero"]["newvalue"]} {stattemp["range"]["newvalue"]} {stattemp["velocity2"]["newvalue"]} {stattemp["penetration1"]["newvalue"]} {stattemp["penetration2"]["newvalue"]} {stattemp["soundrange"]["newvalue"]}")
    
    #UI related stats
    stattemp["ui_accuracy"]["newvalue"] = accuracy or 50 
    stattemp["ui_control"]["newvalue"] = control or 50
    stattemp["ui_range"]["newvalue"] = ((stattemp["range"]["newvalue"]-117)*(100/220))
    stattemp["ui_weight"]["newvalue"] = ((magazineweight+weight)*(100/20))
    stattemp["ui_noise"]["newvalue"] = (stattemp["soundrange"]["newvalue"]*(1/13))
    stattemp["ui_rateoffire"]["newvalue"] = rof
    print(f"UI Values set: {stattemp["ui_accuracy"]["newvalue"]} {stattemp["ui_control"]["newvalue"]} {stattemp["ui_range"]["newvalue"]} {stattemp["ui_weight"]["newvalue"]} {stattemp["ui_noise"]["newvalue"]} {stattemp["ui_rateoffire"]["newvalue"]}")
    
    #Last few meaningful stats
    stattemp["timetoaim"]["newvalue"] = 0.25+(((magazineweight+weight)-1)*(0.5/18))
    if onehanded == 1:
        stattemp["burdenfactor"]["newvalue"] = 2-(((weight+magazineweightmod)-1)*(1.5/18))
    else:
        stattemp["burdenfactor"]["newvalue"] = 1.5-(((weight+magazineweightmod)-1)*(1.5/18))
    stattemp["mobility"]["newvalue"] = 1.3-(((weight+magazineweight)-1)*(0.9/18))
    stattemp["reloadtime"]["newvalue"] = stattemp["reloadtime"]["value"]
    print(f"Remaining Primary stats set: {stattemp["timetoaim"]["newvalue"]} {stattemp["burdenfactor"]["newvalue"]} {stattemp["mobility"]["newvalue"]} {stattemp["reloadtime"]["newvalue"]} ")

    #Spread
    stattemp["sway"]["newvalue"] = 1
    stattemp["modulatedspreadmax"]["newvalue"] = 1
    stattemp["modulatedspreadmin"]["newvalue"] = 1
    stattemp["modulatedspreadironsights"]["newvalue"] = 1
    stattemp["ironsightspreadmultiplier"]["newvalue"] = 1
    stattemp["otsspreadmultiplier"]["newvalue"] = 1
    stattemp["spreadradiusmin"]["newvalue"] = 1
    stattemp["spreadradiusmax"]["newvalue"] = 1
    stattemp["spreadtimetomin"]["newvalue"] = 0
    stattemp["spreadtimetomax"]["newvalue"] = 0

    #Other
    stattemp["projectilebreakingangle"]["newvalue"] = 0.261799
    stattemp["recoilpivot"]["newvalue"] = 5
    stattemp["ui_unknown1"]["newvalue"] = 50
    stattemp["ui_unknown2"]["newvalue"] = 50
    stattemp["tacticalreloadthreshold"]["newvalue"] = 0.85
    stattemp["walkspeedmultiplier"]["newvalue"] = 1
    stattemp["adssensitivity"]["newvalue"] = 1  

    #UI Refresh
    refreshstatnewvalue()

    #Opening apply button
    func.applybtn.config(state="ENABLED")
def applyallwayson():
    global inputboxes
    global stattemp
    for i, b in enumerate(stattemp.items()): # Adding new values from input boxes to dictionary before write.
        inputname = b[0] #Gets the name of the dictionary
        newval = inputboxes[inputname].get() # Gets the value from the inputbox
        stattemp[inputname]["newvalue"] = newval # sets the "newvalue" to the value from the inputbox

    func.writestats() #writes all newvalues to file.
def apply():
    #Skriv til fil
    func.writestats()

    # Deaktiver Apply-knappen
    func.applybtn.config(state="disabled")

#A default window for popups and errors
btntext = {
    "ok": "OK",
    "report": "Report bug",
    "open": "Open",
    "copyu64": "Copy file's u64 value to clipboard",
    "empty": "empty",
    "close": "Exit",
    "ignore": "Ignore",
    "apply": "Apply",
    "calculate": "Calculate",
    "applyallwayson": "Apply",
}
btnfunc = {
    "report": report,
    "open": openfile,
    "copyu64": lambda: copyclipboard(func.fileu64),
    "close": terminateall,
    "apply": apply,
    "calculate": calculate,
    "applyallwayson": applyallwayson,
}
wintype = {
    "error": "Error",
    "warning": "Warning",
    "succes": "Succes",
    "info": "Info"
}
def messagewindow(type, title, message, buttons):
    global root
    global fileu64
    print(f"Opening {type} window: {title} - {message}")
    errorwin = Toplevel(root)
    errorwin.rowconfigure(0, weight=1)
    errorwin.rowconfigure(1, weight=1, minsize=30)
    errorwin.title(title)
    buttonsbottom = ttk.Frame(errorwin)
    buttonsbottom.grid(row=1, column=0, sticky=(E, W), padx=20, pady=5)
    for i, b in enumerate(buttons):
        text = btntext[b]
        if text in ("OK", "Ignore"):
            cmd = errorwin.destroy
        else:
            cmd = btnfunc[b]
        ttk.Button(buttonsbottom, text=text, command=cmd).grid(column=i, row=0)
        buttonsbottom.columnconfigure(i, weight=1)
    if type in ("error", "warning"):
        errormessage = f"{message}\n\nThe report button copies the log to the clipboard and opens the bugpage on nexusmods in your browser. \n\nSimply paste it into a report and tell me what you were doing."
    else:
        errormessage = message
    ttk.Separator(errorwin, orient=HORIZONTAL).grid(row=0, sticky=(E, W, S))
    frame = ttk.Labelframe(errorwin, text=title)
    frame.grid(column=0, row=0, sticky=(N, E, S, W), pady=10, padx=15)
    ttk.Label(
    frame, 
    text=errormessage,
    wraplength=280,
    justify="left"
    ).grid(padx=6, pady=7)
    errorwin.grab_set()
    errorwin.wait_window()



