from core.settings import settings
import customtkinter as ctk

class Button:
    def __init__(self, parent, label, function, state:bool = True):
        if settings == None: # gets backup settings if settings doesnt exist
            self.backupsettings()
        else:
            self.getsettings()
        if isinstance(label, int): # If label is a number get it from settings language. If it isnt, its a string from popup and settings is corrupt/None
            label = settings.language[label]
        self.button = ctk.CTkButton(parent, text=label, command=function,  
        fg_color=self.background, 
        text_color=self.text, 
        border_color=self.border,
        border_width=1,
        corner_radius=5,
        hover_color=self.highlight,
        text_color_disabled=self.darkaccent,
        width=100)
        if state == False:
            self.button.configure(state='disabled')

    def changestate(self, state:bool = True):
        if state == False: # disables button if supplied bool is false
            self.button.configure(state='disable')
            return
        print("enabling button")
        self.button.configure(state='normal') # enables button if supplied bool is true

    def remove(self):
        self.button.destroy()

    def backupsettings(self):
        self.darkaccent = '#333333'
        self.highlight = "#666666"
        self.background = "#222222"
        self.border = "#AAAAAA"
        self.text = "#EEEEEE"
        self.accent = '#555555'

    def getsettings(self):
        self.darkaccent = settings.darkaccent
        self.highlight = settings.highlight
        self.accent = settings.accent
        self.background = settings.background
        self.border = settings.border
        self.text = settings.text

        
            




