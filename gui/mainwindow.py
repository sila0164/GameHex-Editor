import customtkinter as ctk
import core.settings
import core.file as file
import gui.common as gui

class MainWindow:# The main window that contains everything

    def __init__(self):

        # Creates itself
        print('MainWindow: Creating Main Window')
        self.root = ctk.CTk()
        self.root.title(core.settings.current.language[12])
        self.root.geometry("450x600")
        self.main = ctk.CTkFrame(self.root, fg_color=core.settings.current.background)
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
        self.main = ctk.CTkFrame(parent, fg_color=core.settings.current.background,
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
        self.filedisplayframe = ctk.CTkFrame(parent, fg_color=core.settings.current.background,
        corner_radius=0,
        )
        if isinstance(message, int):
            message = core.settings.current.language[message]
        self.filedisplayframe.grid(column=parentcolumn, columnspan=columnspan, row=parentrow, sticky='WNSE')
        self.filedisplay = ctk.CTkLabel(self.filedisplayframe, text=message, bg_color=core.settings.current.background,
        text_color=core.settings.current.text)
        self.filedisplay.grid(column=0, row=0, sticky='W', padx=4)
    
    def changetext(self, message, delayedmessage = None, timer: int = 3500):
        if isinstance(message, int):
            message = core.settings.current.language[message]
        self.filedisplay.configure(text=message)
        self.filedisplay.update_idletasks()
        if delayedmessage != None:
            if isinstance(delayedmessage, int):
                delayedmessage = core.settings.current.language[delayedmessage]
            self.filedisplay.after (timer, lambda: self.filedisplay.configure(text=delayedmessage))

class StatDisplay: # The main data manipulation interface
    def __init__(self, parent: ctk.CTkFrame, parentcolumn: int=2, parentrow: int=2):
        self.main = ctk.CTkScrollableFrame(parent,
        fg_color=core.settings.current.darkaccent,
        scrollbar_fg_color=core.settings.current.background,
        corner_radius=0)
        self.main.grid(row=parentrow, column=parentcolumn, sticky='NSEW')
        self.main.columnconfigure(0, weight=1)
        self.main.columnconfigure(1, weight=0)
    
    def newfile(self, enablewrite): # saves the dictionary to itself
        self.rowcount = 0
        self.revert = {}
        self.originalvalue= {}
        self.lastvalue = {}
        self.revertcount = 0
        self.inputs = {} # keeps track of the inputboxes
        for index, key in enumerate(file.current.stat): # creates an inputbox for each stat in the dictionary
            self.main.rowconfigure(self.rowcount, weight=0) #Configures the row
            value = file.current.stat[key]['value']
            bgcolor = core.settings.current.accent
            colorcalc = self.rowcount / 2
            if colorcalc % 2 == 0: # Makes the backgroundcolor change for every other entry
                bgcolor = core.settings.current.darkaccent
            self.inputs[key] = gui.Inputbox(self.main, self.rowcount, key, value, bgcolor)
            self.inputs[key].valuegetupdates(enablewrite)
            self.originalvalue[key] = value
            self.lastvalue[key] = value
            self.rowcount += 1 # Counts the row up 1
            self.horsep = gui.Separator(self.main, self.rowcount, 0, 2, 'horizontal')
            self.rowcount += 1

    def updaterevert(self, statname):
        key = self.stringvar[statname]
        self.revert[str(self.revertcount)] = {}
        self.revert[str(self.revertcount)]['name'] = key
        self.revert[str(self.revertcount)]['value'] = self.lastvalue[key]
        self.lastvalue[key] = self.inputs[key].getvalue()
        self.revertcount += 1

    def revertlast(self):
        inputname = self.revert[str(self.revertcount)]['name']
        inputoldvalue = self.revert[str(self.revertcount)]['value']
        self.inputs[inputname].value.set(inputoldvalue)
        del self.revert[str(self.revertcount)]
        self.revertcount -= 1

    def revertoriginal(self):
        for index, input in enumerate(self.inputs):
            self.updaterevert(input)
            self.inputs[input].value.set(self.originalvalue[input]) 

    def clear(self):
        for child in self.main.winfo_children():
            child.destroy()

    def sendnewvaluestofile(self) -> bool:
        import core.file as file
        convertfails = 0
        for index, input in enumerate(self.inputs):
            newvalue = self.inputs[input].getvalue()
            type = file.current.stat[input]['type']
            if type == 'float':
                try:
                    newvalue = float(newvalue)
                    print(f'StatDisplay: set {input} as float')
                except:
                    print(f'StatDisplay: could not set {input} as float: {newvalue}')
                    convertfails += 1
            elif 'int' in type:
                try:
                    newvalue = int(newvalue)
                    print(f'StatDisplay: set {input} as int')
                except:
                    print(f'StatDisplay: could not set {input} as int: {newvalue}')
                    convertfails += 1
            if isinstance(newvalue, (float, int)):
                if file.current.stat[input]['value'] != newvalue:
                    print(f'StatDisplay: Sending {input} to write. {file.current.stat[input]['value']} -> {newvalue}')
                    file.current.changevalue(input, newvalue)
        if convertfails > 0:
            return False
        return True
    
    


            
            

