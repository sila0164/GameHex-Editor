from tkinter import ttk
from tkinter import *
import db
import func

#Main window 
def mainwindowinit(windowtitle=None, resolution=None):
    windowtitle = windowtitle or "WABO Conversion Tool"
    resolution = resolution or ""
    print(f"Initalizing main window as {windowtitle}")
    func.root = Tk()
    func.root.title(windowtitle)
    func.root.geometry(resolution)
    func.mainframe = ttk.Frame(func.root)
    func.mainframe.grid(row=0, column=0)
    func.mainframe.rowconfigure(0, weight=1)
    func.mainframe.rowconfigure(1, weight=1)
    func.mainframe.rowconfigure(2, weight=1)
    func.mainframe.rowconfigure(3, weight=1)
    func.buttonsbottom = ttk.Frame(func.mainframe)
    func.buttonsbottom.grid(row=3, column=0, sticky=(E, W))
    func.buttonstop = ttk.Frame(func.mainframe)
    func.buttonstop.grid(row=0, column=0, sticky=(E, W))
def mainwindow(buttonstop=None, buttonsbottom=None, resolution=None):
    resolution = resolution or ""
    print("Changing main window")
    pos = 0
    if buttonstop:
        func.buttonstop.grid(pady=5, padx=5)
        for i, b in enumerate(buttonstop):
            if b == "empty":
                func.buttonstop.columnconfigure(i, weight=1, minsize=30)
            elif b == "apply":
                text = func.btntext[b]
                cmd = func.btnfunc[b]
                func.buttonsbottom.columnconfigure(i, weight=1)
                func.applybtn = ttk.Button(func.buttonsbottom, text=text, command=cmd, state=DISABLED)
                func.applybtn.grid(column=i, row=0)
            else:
                text = func.btntext[b]
                cmd = func.btnfunc[b]
                func.buttonstop.columnconfigure(i, weight=1)
                ttk.Button(func.buttonstop, text=text, command=cmd).grid(column=i, row=0)
            pos += 1
    else:
        func.buttonstop.grid(pady=0, padx=0)
    pos = 0    
    if buttonsbottom:
        func.buttonsbottom.grid(pady=5, padx=5)
        for i, b in enumerate(buttonsbottom):
            if b == "empty":
                func.buttonsbottom.columnconfigure(i, weight=1, minsize=30)
            elif b == "apply":
                text = func.btntext[b]
                cmd = func.btnfunc[b]
                func.buttonsbottom.columnconfigure(i, weight=1)
                func.applybtn = ttk.Button(func.buttonsbottom, text=text, command=cmd, state=DISABLED)
                func.applybtn.grid(column=i, row=0)
            else:
                text = func.btntext[b]
                cmd = func.btnfunc[b]
                func.buttonsbottom.columnconfigure(i, weight=1)
                ttk.Button(func.buttonsbottom, text=text, command=cmd).grid(column=i, row=0)
            pos += 1
    else:
        func.buttonsbottom.grid(pady=0, padx=0)     
def mainwindowreset():
    func.mainframe.destroy()
    func.mainframe = ttk.Frame(func.root)
    func.mainframe.grid(row=0, column=0)
    func.mainframe.rowconfigure(0, weight=1)
    func.mainframe.rowconfigure(1, weight=1)
    func.mainframe.rowconfigure(2, weight=1)
    func.mainframe.rowconfigure(3, weight=1)
    func.buttonsbottom = ttk.Frame(func.mainframe)
    func.buttonsbottom.grid(row=3, column=0, sticky=(E, W))
    func.buttonstop = ttk.Frame(func.mainframe)
    func.buttonstop.grid(row=0, column=0, sticky=(E, W))
#Small display at top of window, for displaying file name and messages
def filedisplayinit():
    print("Initializing file display")
    func.filenamelbl = ttk.Label(func.mainframe)
    func.filenamelbl.grid(column=0, row=1, sticky=(E, W), pady=5, padx=5)
def filedisplay(filetext=None, position=None):
    filetext = filetext or func.filename
    position = position or "left"
    print(f'Changing file display to "{filetext}" --- Postition: {position}')
    if position == "center":
        func.filenamelbl.configure(anchor=position)
    elif position == "left":
        func.filenamelbl.configure(anchor=W)
    elif position == "right":
        func.filenamelbl.configure(anchor=E)
    else:
        print("filedisplay setup incorrectly")
        func.filenamelbl.configure(anchor=LEFT)
    func.filenamelbl.configure(text=filetext)    
#Seperator Initialization
def topseparatorinit():
        func.topsep = ttk.Separator(func.mainframe, orient=HORIZONTAL)
        func.topsep.grid(row=0, sticky=(E, W, S))
def bottomseparatorinit():
        func.bottomsep = ttk.Separator(func.mainframe, orient=HORIZONTAL)
        func.bottomsep.grid(row=3, sticky=(E, W, N))
def extraseperator(row, sticky=None):
        sticky = sticky or "N"
        ttk.Separator(func.mainframe, orient=HORIZONTAL).grid(row=row, sticky=(E, W, sticky))
#Tab configuration
def createtabgroup():
    if hasattr(func, "tabgroup"):
        func.tabgroup.destroy()
    print("Creating Tabgroup")
    func.tabgroup = ttk.Notebook(func.mainframe)
    func.tabgroup.grid(column=0, row=2, sticky=(N, W, E, S), padx=5, pady=5)
def createtab(name):
    tabgroup = func.tabgroup
    print(f"Creating tab {name} in tabgroup")
    frame = ttk.Frame(tabgroup)
    tabgroup.add(frame, text=name)
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)
    func.currenttab = frame
    func.tabrow = 0
def creategroup(name):
    print(f"Creating group {name} in tab")
    frame = ttk.Labelframe(func.currenttab, text=name)
    frame.grid(column=0, row=func.tabrow, sticky=(N, E, W, S), pady=10, padx=10)
    frame.columnconfigure(0, weight=1, minsize=200)
    frame.columnconfigure(1, weight=1, minsize=50)
    frame.columnconfigure(2, weight=1, minsize=50)
    frame.rowconfigure(0, weight=0)
    func.currentgroup = frame
    func.tabrow += 1
    func.grouprow = 0
def createdropdown(stat):
    print(f"Creating {stat} in Group")
    name = func.statdict[stat]
    newvalue = func.stattemp[stat]["refname"]
    if func.grouprow != 0:
        func.currentgroup.rowconfigure(func.grouprow, weight=0)
        ttk.Separator(func.currentgroup, orient=HORIZONTAL).grid(column=0, row=func.grouprow, columnspan=3, sticky=(E, W), padx=5)
        func.grouprow += 1
    func.currentgroup.rowconfigure(func.grouprow, weight=0)
    ttk.Label(func.currentgroup, text=name).grid(column=0, row=func.grouprow, pady=2, sticky=W, padx=6)
    currentdict = getattr(db, stat)
    options = list(currentdict.keys())
    combobox = ttk.Combobox(func.currentgroup, values=options, state="readonly")
    combobox.grid(column=2, row=func.grouprow, sticky=E, padx=6) 
    combobox.set(newvalue)
    func.inputboxes[stat] = combobox
    func.grouprow += 1

    if stat == "ammotype":
        func.currentgroup.rowconfigure(func.grouprow, weight=0)
        ttk.Separator(func.currentgroup, orient=HORIZONTAL).grid(column=0, row=func.grouprow, columnspan=3, sticky=(E, W), padx=5)
        func.grouprow += 1
        func.currentgroup.rowconfigure(func.grouprow, weight=0)
        ttk.Label(func.currentgroup, text="Barrel Length").grid(column=0, row=func.grouprow, pady=2, sticky=W, padx=6)
        barrel_cb = ttk.Combobox(func.currentgroup, values=[], state="readonly")
        barrel_cb.grid(column=2, row=func.grouprow, sticky=E, padx=6)
        func.inputboxes["barrels"] = barrel_cb
        func.grouprow += 1
        # Barrels specifically
        def update_barrels(event=None, cb=combobox, barrel_cb=barrel_cb):
            selected_ammo = cb.get()
            barrels = []
            ammo_data = getattr(db, "ammotype").get(selected_ammo, {})
            if isinstance(ammo_data, dict) and "barrels" in ammo_data:
                barrels = list(ammo_data["barrels"].keys())
            barrel_cb["values"] = barrels
            barrel_cb.set(barrels[0] if barrels else "")
        combobox.bind("<<ComboboxSelected>>", update_barrels)
        update_barrels()
def createstatlist(stats):
    for i, s in enumerate(stats):
        print(f"Creating {s} in group")
        name = func.statdict[s]
        value = func.stattemp[s]["value"]
        newvalue = func.stattemp[s]["newvalue"]
        if func.grouprow != 0:
            func.currentgroup.rowconfigure(func.grouprow, weight=0)
            ttk.Separator(func.currentgroup, orient=HORIZONTAL).grid(column=0, row=func.grouprow, columnspan=3, sticky=(E, W), padx=5)    
            func.grouprow += 1
        if isinstance(value, float):
            value = f"{value:.2f}"
        if isinstance(newvalue, float):
            newvalue = f"{newvalue:.2f}"
        func.currentgroup.rowconfigure(func.grouprow, weight=0)
        ttk.Label(func.currentgroup, text=name).grid(column=0, row=func.grouprow, pady=2, sticky=W, padx=6)
        lblvalue = ttk.Label(func.currentgroup, text=value)
        lblvalue.grid(column=1, row=func.grouprow, sticky=E)
        lblnewvalue = ttk.Label(func.currentgroup, text=newvalue)
        lblnewvalue.grid(column=2, row=func.grouprow, sticky=E, padx=6)
        func.grouprow += 1
        func.stattemp[s]["labels"] = {
            "current": lblvalue,
            "new": lblnewvalue
        }
def createinputbox(stat):
    print(f"Creating {stat} in group")
    try:
        name = func.statdict[stat]
    except:
        name = stat
    if func.grouprow != 0:
        func.currentgroup.rowconfigure(func.grouprow, weight=0)
        ttk.Separator(func.currentgroup, orient=HORIZONTAL).grid(column=0, row=func.grouprow, columnspan=3, sticky=(E, W), padx=5)
        func.grouprow += 1    
    func.currentgroup.rowconfigure(func.grouprow, weight=0)
    ttk.Label(func.currentgroup, text=name).grid(column=0, row=func.grouprow, pady=2, sticky=W, padx=6)
    try:
        value = func.stattemp[stat]["value"]
        if isinstance(value, float):
            value = f"{value:.2f}"
        ttk.Label(func.currentgroup, text=value).grid(column=1, row=func.grouprow, sticky=E)
    except:
        pass
    try:
        newvalue = func.stattemp[stat]["newvalue"]
        if isinstance(newvalue, float):
            newvalue = f"{newvalue:.2f}"
    except:
        newvalue = 0
    var = StringVar()
    var.set(newvalue)
    entrybox = ttk.Entry(func.currentgroup, textvariable=var)
    entrybox.grid(column=2, row=func.grouprow, sticky=E, padx=6)
    func.grouprow += 1
    func.inputboxes[stat] = var
def createcheckbox(stat):
    var = IntVar(value=0)
    print(f"Creating checkbox {stat} in group")
    if func.grouprow != 0:
        func.currentgroup.rowconfigure(func.grouprow, weight=0)
        ttk.Separator(func.currentgroup, orient=HORIZONTAL).grid(column=0, row=func.grouprow, columnspan=3, sticky=(E, W), padx=5)    
        func.grouprow += 1
    func.currentgroup.rowconfigure(func.grouprow, weight=0)
    ttk.Label(func.currentgroup, text=stat).grid(column=0, row=func.grouprow, pady=2, sticky=W, padx=6)
    checkbox = ttk.Checkbutton(func.currentgroup, variable=var)
    checkbox.grid(column=2, row=func.grouprow, sticky=E, padx=6)
    func.grouprow += 1
    setattr(func, stat, var)
