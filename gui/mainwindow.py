import customtkinter as ctk
from core.settings import settings
from gui.common import Inputbox

class MainWindow:# The main window that contains everything

    def __init__(self):

        # Creates itself
        print('MainWindow: Creating Main Window')
        self.root = ctk.CTk()
        self.root.title(settings.language[12])
        self.root.geometry("450x600")
        self.main = ctk.CTkFrame(self.root, bg_color=settings.background)
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
        self.horseparator = ctk.CTkFrame(self.main, height=1, fg_color=settings.border)
        self.horseparator.grid(row=1, column=0, columnspan=3, sticky='EW')
        self.verseparator = ctk.CTkFrame(self.main, width=1, fg_color=settings.border)
        self.verseparator.grid(row=2, column=1, sticky='SN')

    def exit(self):
        self.root.destroy()

class ButtonBox: # The box on the left side of the window containing the buttons
    def __init__(self, parent, parentcolumn: int=0, parentrow: int=2):
        self.main = ctk.CTkFrame(parent, fg_color=settings.background,
        corner_radius=0)
        self.main.grid(row=parentrow, column=parentcolumn, sticky='NSEW')
        for row in range(11):
            if row == 8: # Makes the row before last fill any empty space, to create a neater interface
                self.main.rowconfigure(8, weight=100)
            else:
                self.main.rowconfigure(row, weight=1)
        self.buttons = {} # a list of buttons
        self.buttoncount = 0 # a counter of buttons, to automatically create buttons without needing to get row number

    def placebutton(self, button, row=None): 
        if row == None: # automatically sets row to next row if no row has been supplied
            row = self.buttoncount
            self.buttoncount += 1
        
        button.grid(column=0, row=row, padx=4, pady=4) # places button in specific row

class FileDisplay: # The text/message display at the top of the window
        
    def __init__(self, message, parent: ctk.CTkFrame, parentcolumn: int=0, parentrow: int=0, columnspan: int=1000):
        self.filedisplayframe = ctk.CTkFrame(parent, fg_color=settings.background,
        corner_radius=0,
        )
        if isinstance(message, int):
            message = settings.language[message]
        self.filedisplayframe.grid(column=parentcolumn, columnspan=columnspan, row=parentrow, sticky='WNSE')
        self.filedisplay = ctk.CTkLabel(self.filedisplayframe, text=message, bg_color=settings.background,
        text_color=settings.text)
        self.filedisplay.grid(column=0, row=0, sticky='W', padx=4)
    
    def changetext(self, message, delayedmessage = None, timer: int = 3500):
        if isinstance(message, int):
            message = settings.language[message]
        self.filedisplay.configure(text=message)
        self.filedisplay.update_idletasks()
        if delayedmessage != None:
            if isinstance(delayedmessage, int):
                delayedmessage = settings.language[delayedmessage]
            self.filedisplay.after (timer, lambda: self.filedisplay.configure(text=delayedmessage))

class StatDisplay: # The main data manipulation interface
    def __init__(self, parent: ctk.CTkFrame, enablewrite, parentcolumn: int=2, parentrow: int=2):
        self.main = ctk.CTkScrollableFrame(parent,
        fg_color=settings.darkaccent,
        scrollbar_fg_color=settings.background,
        corner_radius=0)
        self.main.grid(row=parentrow, column=parentcolumn, sticky='NSEW')
        self.main.columnconfigure(0, weight=1)
        self.main.columnconfigure(1, weight=0)
        self.rowcount = 0
        self.enablewrite = enablewrite

    def update(self): # saves the dictionary to itself
        import core.file as file
        self.inputs = {} # keeps track of the inputboxes
        for index, key in enumerate(file.current.stat): # creates an inputbox for each stat in the dictionary
            self.main.rowconfigure(self.rowcount, weight=0) #Configures the row
            value = file.current.stat[key]['value']
            bgcolor = settings.accent
            colorcalc = self.rowcount / 2
            if colorcalc % 2 == 0: # Makes the backgroundcolor change for every other entry
                bgcolor = settings.darkaccent
            self.inputs[key] = Inputbox(self.main, self.rowcount, key, value, bgcolor)
            self.inputs[key].valueupdate(self.enablewrite)
            self.rowcount += 1 # Counts the row up 1
            self.horseparator = ctk.CTkFrame(self.main, height=1, fg_color=settings.border)
            self.horseparator.grid(row=self.rowcount, column=0, columnspan=2, sticky='EW')
            self.rowcount += 1
    
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
    
    


            
            

