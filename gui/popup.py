import customtkinter as ctk
from gui.common import Button
import core.settings

popupdefault = {
    0: 'Close',
    1: 'ERROR: Could not read settings',
    2: 'Could not read or create "Settings.json".\n\nTry deleting it from the folder the .exe is in, if it already exists.',
    3: "",
    4: "This shouldn't exist",
    8: 'Could not read "Settings.json".\n\nIt is either corrupt, or something isnt in the correct syntax. Do you want to overwrite it and create a new one?',
    9: 'Yes',
    10: 'No',
}

class Popup:
    
    def __init__(self, title, message, root=None, report: bool=False, backup:bool=False):
        if backup == True: # gets backup settings 
            self.backupsettings(message)
        else:
            self.getsettings(title, message)
        finalmessage = self.message
        print(f'Popup: Creating {self.title}')
        if root == None: # creates itself as root if there is none
            print('Popup: Running as main root')
            self.root = ctk.CTk()
        else: # goes toplevel of root if there is a window open.
            print('Popup: Running as Toplevel')
            self.root = ctk.CTkToplevel(root)
        
        self.report = False
        if report == True: # adds the report bug text to the message if it is true
            print('Popup: Report button enabled')
            self.report = True
            finalmessage = (f'{self.message}{self.dict[3]}')
        
        self.root.title(self.title)
        self.main = ctk.CTkFrame(self.root, 
        fg_color=self.darkaccent,
        corner_radius=0)
        self.main.grid(row=0, column=0, sticky='NSEW')
        self.main.rowconfigure(0, weight=1)
        self.main.rowconfigure(1, weight=1, minsize=70)
        self.buttonbox = ctk.CTkFrame(self.main,
        fg_color=self.background,
        corner_radius=0)
        self.buttonbox.grid(row=1, column=0, sticky='NSEW')
        self.buttonbox.rowconfigure(0, weight=1)
        self.messageframe = ctk.CTkFrame(self.main, fg_color=self.darkaccent, 
        border_color=self.border,
        border_width=1,
        corner_radius=5)
        self.messageframe.grid(column=0, row=0, sticky='NESW', pady=25, padx=25,)
        ctk.CTkLabel(
        self.messageframe, 
        text=finalmessage,
        wraplength=280,
        justify="left",
        text_color=self.text
        ).grid(padx=6, pady=7)
        self.horseparator = ctk.CTkFrame(self.main, height=1, fg_color=self.border)
        self.horseparator.grid(row=1, column=0, columnspan=3, sticky='NEW')
    
    def backupsettings(self, message):
        print('Popup: Getting backup settings')
        self.darkaccent = '#333333'
        self.highlight = "#666666"
        self.background = "#222222"
        self.border = "#AAAAAA"
        self.text = "#EEEEEE"
        self.dict = popupdefault
        self.message = popupdefault[message]
        self.title = popupdefault[1]
    
    def getsettings(self, title, message):
        print('Popup: Getting settings from core')
        self.darkaccent = core.settings.current.darkaccent
        self.highlight = core.settings.current.highlight
        self.background = core.settings.current.background
        self.border = core.settings.current.border
        self.text = core.settings.current.text
        self.dict = core.settings.current.language
        self.message = self.dict[message]
        self.title = self.dict[title]

    def close(self):
        if isinstance(self.root, ctk.CTk):
            self.root.update_idletasks()
        self.root.destroy()

    def buttonsbool(self, truelabel: int, falselabel: int) -> bool: 
        # Creates button
        self.returnbool = False
        def true():
            print('Popup: Player selected true')
            self.returnbool = True
            self.close()
        def false():
            print('Popup: Player selected false')
            self.returnbool = False
            self.close()
        #Buttons
        print(f'Popup: Creating buttonsbool: {self.dict[truelabel]} - {self.dict[falselabel]}')
        self.true = Button(self.buttonbox, label=self.dict[truelabel], function=true)
        self.false = Button(self.buttonbox, label=self.dict[falselabel], function=false)
        
        self.buttonbox.columnconfigure(0, weight=1)
        self.true.button.grid(column=0, row=0, padx=4, pady=4)
        
        self.buttonbox.columnconfigure(1, weight=1)
        self.false.button.grid(column=1, row=0, padx=4, pady=4)
        # Makes the window force the user to choose
        if isinstance(self.root, ctk.CTk):
            self.root.mainloop()
        else:
            self.root.grab_set()
            self.root.wait_window()
        return self.returnbool

    def buttonsackknowledge(self, label: int):
        def ok():
            self.close()
        # true button
        print(f'Popup: Creating buttonsackknowledge: {self.dict[label]}')
        self.ok = Button(self.buttonbox, label=self.dict[label], function=ok)
        # places button in specific row
        self.buttonbox.columnconfigure(0, weight=1)
        self.ok.button.grid(column=0, row=0, padx=4, pady=4) 
        if isinstance(self.root, ctk.CTk):
            self.root.mainloop()
        else:
            self.root.grab_set()
            self.root.wait_window()

