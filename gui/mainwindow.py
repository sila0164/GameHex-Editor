import customtkinter as ctk
import core
from core import error, dev
import gui.common as gui

class MainWindow:# The main window that contains everything

    def __init__(self):

        # Creates itself
        self.root = ctk.CTk()
        self.root.title(core.settings.language[12])
        if core.settings.debug == False:
            self.root.geometry("600x600")
        else:
            self.root.geometry("700x600")
        self.root.iconbitmap("gui/icon.ico")
        self.main = ctk.CTkFrame(self.root, fg_color=core.settings.background)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main.columnconfigure(0, weight=0)
        self.main.columnconfigure(1, weight=0)
        self.main.columnconfigure(2, weight=1)
        self.main.rowconfigure(0, weight=0)
        self.main.rowconfigure(1, weight=0)
        self.main.rowconfigure(2, weight=1)

        # Creates the white lines that seperate items on screen
        self.horsep = gui.Separator(self.main, 1, 0, 3, 'horizontal')
        self.versep = gui.Separator(self.main, 1, 1, 2, 'vertical')

    def unhide(self):
        self.main.grid(row=0, column=0, sticky='NSEW')

    def exit(self):
        self.root.destroy()

class ButtonBox: # The box on the left side of the window containing the buttons
    def __init__(self, parent, parentcolumn: int=0, parentrow: int=2):
        self.main = ctk.CTkFrame(parent, fg_color=core.settings.background,
        corner_radius=0, border_width=0)
        self.main.grid(row=parentrow, column=parentcolumn, sticky='NSEW')
        self.buttoncount = 0 # a counter of buttons, to automatically create buttons without needing to get row number

    def placebutton(self, button, lastbutton:bool=False): 
        if lastbutton == True:
            self.main.rowconfigure(self.buttoncount, weight=100)
            self.buttoncount += 1
        self.main.rowconfigure(self.buttoncount, weight=0)
        button.grid(column=0, row=self.buttoncount, padx=4, pady=4)
        self.buttoncount += 1
    
    def space(self, space:int=15):
        self.main.rowconfigure(self.buttoncount, weight=0, minsize=space)
        self.buttoncount += 1

class FileDisplay: # The text/message display at the top of the window
        
    def __init__(self, message, parent: ctk.CTkFrame, parentcolumn: int=0, parentrow: int=0, columnspan: int=1000):
        self.filedisplayframe = ctk.CTkFrame(parent, fg_color=core.settings.background,
        corner_radius=0,
        )
        if isinstance(message, int):
            message = core.settings.language[message]
        self.filedisplayframe.grid(column=parentcolumn, columnspan=columnspan, row=parentrow, sticky='WNSE')
        self.filedisplay = ctk.CTkLabel(self.filedisplayframe, text=message, bg_color=core.settings.background,
        text_color=core.settings.text, justify='left', anchor='w')
        self.filedisplay.grid(column=0, row=0, sticky='W', padx=4)
    
    def changetext(self, message, wait: bool = False, delayedmessage = None, timer: int = 3500):
        if isinstance(message, int):
            message = core.settings.language[message]
        self.filedisplay.configure(text=message)
        if delayedmessage != None:
            if isinstance(delayedmessage, int):
                delayedmessage = core.settings.language[delayedmessage]
            self.filedisplay.after (timer, lambda: self.filedisplay.configure(text=delayedmessage))

class StatDisplay: # The main data manipulation interface
    def __init__(self, parent: ctk.CTkFrame, parentcolumn: int=2, parentrow: int=2):
        self.main = ctk.CTkScrollableFrame(parent,
        fg_color=core.settings.darkaccent,
        scrollbar_fg_color=core.settings.background,
        corner_radius=0)
        self.main.grid(row=parentrow, column=parentcolumn, sticky='NSEW')
        self.main.columnconfigure(0, weight=1)
        self.main.columnconfigure(1, weight=0)
        self.revertlastisactive = False
        self.revertoriginalisactive = False
    
    def newfile(self, enablewrite, file: core.File):
        dev('StatDiplay: Creating entries')
        self.main.grid_remove()
        self.rowcount = 0
        self.revert = {}
        self.separators = {}
        self.revertcount = 0
        self.inputs = {} # keeps track of the inputboxes
        self.inputamount = 0
        for id in file.stat: # creates an inputbox for each stat in the dictionary
            self.main.rowconfigure(self.rowcount, weight=0) #Configures the row
            value = file.stat[id]['value']
            title = file.stat[id]['title']
            type = file.stat[id]['type']
            offset = file.stat[id]['offset']
            bgcolor = core.settings.accent
            colorcalc = self.rowcount / 2
            if colorcalc % 2 == 0: # Makes the backgroundcolor change for every other entry
                bgcolor = core.settings.darkaccent
            if file.stat[id]['dict'] != None:
                dictionary = file.stat[id]['dict']
                self.inputs[id] = gui.Dropdown(self.main, self.rowcount, title, id, value, type, offset, dictionary, backgroundcolor=bgcolor)
            else:
                self.inputs[id] = gui.Inputbox(self.main, self.rowcount, title, id, value, type, offset, bgcolor)
            self.inputs[id].valuegetupdates(enablewrite)
            self.rowcount += 1 # Counts the row up 1
            self.separators[self.rowcount] = gui.Separator(self.main, self.rowcount, 0, 2, 'horizontal')
            self.rowcount += 1
        self.main.after_idle(self.unhideinputs)
        
    def unhideinputs(self):
        for input in self.inputs:
            dev(f'StatDisplay: Unhiding {input}')
            self.inputs[input].unhide()
        self.main.grid()

    def updaterevertlog(self, value_id):
        if self.revertlastisactive == True: # To stop it updating and ruining the revertcount order, when reverting. Or if the input returns None(Dropdown does but updates twice)
            return
        new_value = self.inputs[value_id].getvalue()
        dev(f'Statdisplay: Update value: {value_id} - {new_value}')
        duplicatecheck = self.revertcount - 1
        if self.revertcount > 0 and self.revert[str(duplicatecheck)]['name'] == value_id:
            dev(f'StatDisplay: Ignoring revert log input, its already been updated')
            return # This stops it from creating 10 entries for every little change in a box. Just saves the value at first change.
        self.revert[str(self.revertcount)] = {}
        self.revert[str(self.revertcount)]['name'] = value_id
        self.revert[str(self.revertcount)]['value'] = self.inputs[value_id].lastvalue
        self.revertcount += 1
        dev(f'StatDisplay: Revert log: {self.revert}')

    def revertlast(self):
        self.revertlastisactive = True
        dev(f'StatDisplay: Before Revert: {self.revertcount}')
        numberinlist = self.revertcount - 1
        inputname = self.revert[str(numberinlist)]['name']
        inputoldvalue = self.revert[str(numberinlist)]['value']
        self.inputs[inputname].valueset(inputoldvalue)
        del self.revert[str(numberinlist)]
        self.revertcount -= 1
        self.revertlastisactive = False
        dev(f'StatDisplay: After Revert: {self.revertcount}')
        dev(f'StatDisplay: Revert log: {self.revert}')

    def state_toggleall(self):
        for input in self.inputs:
            dev(f'StatDisplay: toggling {input}')
            self.inputs[input].toggle()

    def clear(self):
        dev('StatDisplay: Clearing')
        self.main.grid_remove()
        for input in self.inputs:
            dev(input)
            self.inputs[input].clear()
        for sep in self.separators:
            dev(sep)
            self.separators[sep].main.destroy()
        self.main.grid()

    def getvalue(self, value_id: str = '', all: bool = False) -> int | float | str | list:
        if all == True:
            dev(f'StatDisplay: getting values, current inputs: {self.inputs.keys()}')
            values = []
            for input in self.inputs:
                value = self.inputs[input].getvalue()
                values.append(value)
            return values
        value = self.inputs[value_id].getvalue()
        return value


    
    


            
            

