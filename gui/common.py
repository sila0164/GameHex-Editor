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
        self.name = label
        print(f'Button: Creating {self.name}')
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
            print(f"Button: disabling {self.name}")

    def changestate(self, state:bool = True):
        if state == False: # disables button if supplied bool is false
            print(f"Button: disabling button {self.name}")
            self.button.configure(state='disable')
            return
        print(f"Button: enabling button {self.name}")
        self.button.configure(state='normal') # enables button if supplied bool is true

    def remove(self):
        print(f'Button: destroying {self.name}')
        self.button.destroy()

    def backupsettings(self):
        self.darkaccent = '#333333'
        self.highlight = "#666666"
        self.background = "#222222"
        self.border = "#AAAAAA"
        self.text = "#EEEEEE"
        self.accent = '#444444'

    def getsettings(self):
        self.darkaccent = settings.darkaccent
        self.highlight = settings.highlight
        self.accent = settings.accent
        self.background = settings.background
        self.border = settings.border
        self.text = settings.text

class Inputbox:
    def __init__(self, parent, row, name, value, backgroundcolor):
        print(f'InputBox: Creating {name} with value: {value}')

        self.name = name
        
        self.main = ctk.CTkFrame(parent,
        fg_color=backgroundcolor, # creates the frame
        corner_radius=0)

        self.main.grid(column=0, row=row, sticky='NSEW') # places it in the parent

        self.main.columnconfigure(0, weight=0)
        self.main.columnconfigure(1, weight=1)
        self.main.columnconfigure(2, weight=0)

        self.title = ctk.CTkLabel(self.main, text_color=settings.text, fg_color=backgroundcolor,
            text=name)
        self.title.grid(column=0, row=0, sticky='W', padx=4, pady=1)
        
        self.value = ctk.StringVar()
        self.value.set(value)
        self.input = ctk.CTkEntry(self.main, textvariable=self.value, fg_color=backgroundcolor,
                                  text_color=settings.text,
                                  border_color=settings.border,
                                  width=100,
                                  height=15)
        self.input.grid(column=2, row=0, sticky='E', padx=4, pady=1)

    def clear(self):
        print(f'InputBox: Destroying {self.name}')
        self.main.destroy()

    def getvalue(self):
        print(f'InputBox: Sending {self.name} new value: {self.input.get()}')
        newval = self.input.get()
        newval = newval.replace(',', '.')
        return newval


            




