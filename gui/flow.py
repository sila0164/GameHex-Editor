from gui import *
from core.settings import *


def apply(window): #Needs updating: does nothing currently
    #Skriv til fil
    #func.writestats()
    # Deaktiver Apply-knappen
    window.btnapply.disable()

def copyclipboard(window, string:str):
    root = window.root
    print(f"Copying {string} to clipboard")
    root.clipboard_clear()        
    root.clipboard_append(string)  
    root.update()   

def report(window): #Needs Updating: new webpage
    print("Reporting bug") 
    import webbrowser
    copyclipboard(window, out)
    webbrowser.open("https://www.nexusmods.com/ghostreconbreakpoint/mods/1585?tab=bugs")

def openfile(window):

buttonfunction = {
    #"copyu64": lambda: copyclipboard(fileu64),
    "close": terminate,
    "apply": apply,
    "revert": None,
    "revertoriginal": None,
    "report": report,
    #"calculate": calculate,
}