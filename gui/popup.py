import customtkinter as ctk
from core.settings import settings
from gui.common import Button

popupdefault = {
    0: 'Close',
    1: 'ERROR: Could not read settings',
    2: 'Could not read or create "Settings.json".\n\nTry deleting it from the folder the .exe is in, if it already exists.',
    3: "\n\nThe report button copies the log to the clipboard and opens the bugpage on nexusmods in your browser. Simply paste it into a report and tell me what you were doing.",
    4: 'Report bug',
}

class Popup:
    
    def __init__(self, title, message, root=None, report: bool=False):
        print(f"Creating popup")
        if settings == None: # gets backup settings if settings doesnt exist
            self.backupsettings()
        else:
            self.getsettings(title, message)
        finalmessage = self.message
        if root == None: # creates itself as root if there is none
            self.root = ctk.CTk()
        else: # goes toplevel of root if there is a window open.
            self.root = ctk.CTkToplevel(root)
        
        self.report = False
        if report == True: # adds the report bug text to the message if it is true
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
    
    def backupsettings(self):
        self.darkaccent = '#333333'
        self.highlight = "#666666"
        self.background = "#222222"
        self.border = "#AAAAAA"
        self.text = "#EEEEEE"
        self.dict = popupdefault
        self.message = popupdefault[2]
        self.title = popupdefault[1]
    
    def getsettings(self, title, message):
        self.darkaccent = settings.darkaccent
        self.highlight = settings.highlight
        self.background = settings.background
        self.border = settings.border
        self.text = settings.text
        self.dict = settings.language
        self.message = self.dict[message]
        self.title = self.dict[title]

    def buttonsbool(self, truelabel: int, falselabel: int): 
        # Creates button
        self.returnbool = False
        def true():
            self.returnbool = True
            self.root.destroy()
        def false():
            self.returnbool = False
            self.root.destroy()
        #Buttons
        self.true = Button(self.buttonbox, label=self.dict[truelabel], function=true)
        self.false = Button(self.buttonbox, label=self.dict[falselabel], function=false)
        
        self.buttonbox.columnconfigure(0, weight=1)
        self.true.button.grid(column=0, row=0, padx=4, pady=4)
        
        self.buttonbox.columnconfigure(1, weight=1)
        self.false.button.grid(column=1, row=0, padx=4, pady=4)
        # report button
        if self.report == True:
            self.reportbtn = Button(self.buttonbox, label=self.dict[4], function=self.reportbutton)
            self.buttonbox.columnconfigure(2, weight=1)
            self.reportbtn.button.grid(column=2, row=0, padx=4, pady=4)  
        # Makes the window force the user to choose
        if isinstance(self.root, ctk.CTk):
            self.root.mainloop()
        else:
            self.root.grab_set()
            self.root.wait_window()
        return self.returnbool

    def buttonsackknowledge(self, label: int):
        def ok():
            self.root.destroy()
        # true button
        self.ok = Button(self.buttonbox, label=self.dict[label], function=ok)
        # places button in specific row
        self.buttonbox.columnconfigure(0, weight=1)
        self.ok.button.grid(column=0, row=0, padx=4, pady=4)
        # report button
        if self.report == True:
            self.reportbtn = Button(self.buttonbox, label=self.dict[4], function=self.reportbutton)
            self.buttonbox.columnconfigure(1, weight=1)
            self.reportbtn.button.grid(column=1, row=0, padx=4, pady=4)  
        if isinstance(self.root, ctk.CTk):
            self.root.mainloop()
        else:
            self.root.grab_set()
            self.root.wait_window()

    def reportbutton(self):
        print("Reporting bug") 
        import webbrowser
        from core.file import current
        if current !=None: # Adds print of current file if one is mounted
            log = settings.getlog(current)
        else: # else it just prints the current log
            log = settings.getlog()
        self.root.clipboard_clear()        
        self.root.clipboard_append(log)  
        self.root.update()   
        webbrowser.open("https://www.nexusmods.com/ghostreconbreakpoint/mods/1585?tab=bugs")