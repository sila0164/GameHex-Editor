import customtkinter as ctk
import core
import gui.common as gui

class MainWindow:# The main window that contains everything

    def __init__(self):

        # Creates itself
        self.root = ctk.CTk()
        self.root.title(core.settings.language[12])
        self.root.geometry("600x600")
        self.root.iconbitmap("gui/icon.ico")
        self.main = ctk.CTkFrame(self.root, fg_color=core.settings.background)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main.grid(row=0, column=0, sticky='NSEW')
        self.main.columnconfigure(0, weight=0)
        self.main.columnconfigure(1, weight=0)
        self.main.columnconfigure(2, weight=1)
        self.main.rowconfigure(0, weight=0)
        self.main.rowconfigure(1, weight=0)
        self.main.rowconfigure(2, weight=1)

        # Creates the white lines that seperate items on screen
        self.horsep = gui.Separator(self.main, 1, 0, 3, 'horizontal')
        self.versep = gui.Separator(self.main, 1, 1, 2, 'vertical')

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
        text_color=core.settings.text)
        self.filedisplay.grid(column=0, row=0, sticky='W', padx=4)
    
    def changetext(self, message, delayedmessage = None, timer: int = 3500):
        if isinstance(message, int):
            message = core.settings.language[message]
        self.filedisplay.configure(text=message)
        self.filedisplay.update_idletasks()
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
        self.file = file
        self.rowcount = 0
        self.revert = {}
        self.originalvalue= {}
        self.lastvalue = {}
        self.separators = {}
        self.revertcount = 0
        self.inputs = {} # keeps track of the inputboxes
        self.inputamount = 0
        for index, key in enumerate(self.file.stat): # creates an inputbox for each stat in the dictionary
            self.main.rowconfigure(self.rowcount, weight=0) #Configures the row
            value = self.file.stat[key]['value']
            typename = self.file.stat[key]['typename']
            bgcolor = core.settings.accent
            colorcalc = self.rowcount / 2
            if colorcalc % 2 == 0: # Makes the backgroundcolor change for every other entry
                bgcolor = core.settings.darkaccent
            self.inputamount += 1
            inputname = str(self.inputamount)
            if self.file.stat[key]['dict'] != None:
                dictionary = self.file.stat[key]['dict']
                self.inputs[inputname] = gui.Dropdown(self.main, self.rowcount, key, inputname, value, typename, dictionary, backgroundcolor=bgcolor)
            else:
                self.inputs[inputname] = gui.Inputbox(self.main, self.rowcount, key, inputname, value, typename, bgcolor)
            self.inputs[inputname].valuegetupdates(enablewrite)
            self.originalvalue[inputname] = value
            self.lastvalue[inputname] = value
            self.rowcount += 1 # Counts the row up 1
            self.separators[self.rowcount] = gui.Separator(self.main, self.rowcount, 0, 2, 'horizontal')
            self.rowcount += 1

    def updaterevert(self, statname):
        newval = self.inputs[statname].getvalue()
        if self.revertlastisactive == True or newval == None: # To stop it updating and ruining the revertcount order, when reverting. Or if the input returns None(Dropdown does but updates twice)
            return
        if self.revertoriginalisactive == False:
            duplicatecheck = self.revertcount - 1
            if self.revertcount > 0 and self.revert[str(duplicatecheck)]['name'] == statname:
                self.lastvalue[statname] = newval
                core.debug(f'StatDisplay: Revert log: {self.revert}')
                return # This stops it from creating 10 entries for every little change in a box. Just saves the value at first change.
        self.revert[str(self.revertcount)] = {}
        self.revert[str(self.revertcount)]['name'] = statname
        self.revert[str(self.revertcount)]['value'] = self.lastvalue[statname]
        self.lastvalue[statname] = newval
        self.revertcount += 1
        core.debug(f'StatDisplay: Revert log: {self.revert}')

    def revertlast(self):
        self.revertlastisactive = True
        core.debug(f'StatDisplay: Before Revert: {self.revertcount}')
        numberinlist = self.revertcount - 1
        inputname = self.revert[str(numberinlist)]['name']
        inputoldvalue = self.revert[str(numberinlist)]['value']
        self.inputs[inputname].valueset(inputoldvalue)
        self.lastvalue[inputname] = inputoldvalue
        del self.revert[str(numberinlist)]
        self.revertcount -= 1
        self.revertlastisactive = False
        core.debug(f'StatDisplay: After Revert: {self.revertcount}')

    def revertoriginal(self):
        self.revertoriginalisactive = True
        for index, input in enumerate(self.inputs):
            currentvalue = self.inputs[input].getvalue()
            originalvalue = self.originalvalue[input]
            if currentvalue != originalvalue:
                core.debug(f'StatDisplay: revertoriginal: in box: {currentvalue} - original: {originalvalue}')
                self.inputs[input].value.set(originalvalue)
        self.revertoriginalisactive = False

    def state_toggleall(self):
        for index, input in enumerate(self.inputs):
            self.inputs[input].toggle()

    def clear(self):
        for index, input in enumerate(self.inputs):
            self.inputs[input].clear()
        for index, sep in enumerate(self.separators):
            self.separators[sep].main.destroy()

    def sendnewvaluestofile(self):
        try:
            for index, input in enumerate(self.inputs):
                newvalue = self.inputs[input].getvalue()
                key = self.inputs[input].title
                if self.file.stat[key]['value'] != newvalue:
                    core.debug(f'StatDisplay: Sending {key} to write. {self.file.stat[key]['value']} -> {newvalue}')
                    self.file.changevalue(key, newvalue)
            return True
        except Exception as e:
            core.debug(f'StatDisplay: Error: {e}')
            return False
    
    


            
            

