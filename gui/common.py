import core
import customtkinter as ctk
import tkinter as tk

class Button:
    def __init__(self, parent, label, function, state:bool = True):
        self.getsettings()
        if isinstance(label, int): # If label is a number get it from settings language. If it isnt, its a string from popup and settings is corrupt/None
            label = core.settings.language[label]
        self.name = label
        core.debug(f'Button: Creating "{self.name}" with state: {state}')
        self.button = ctk.CTkButton(parent, text=label, command=function,
        fg_color=self.background, 
        text_color=self.text, 
        border_color=self.border,
        border_width=2,
        corner_radius=5,
        hover_color=self.highlight,
        text_color_disabled=self.darkaccent,
        width=100)
        if state == False:
            self.button.configure(state='disabled')

    def changestate(self, state:bool = True):
        currentstate = self.button._state # Mostly to avoid spam in terminal. Also stops any undesired behaviour in ui
        if state == False and currentstate == 'normal': # disables button if supplied bool is false
            core.debug(f"Button: disabling button {self.name}")
            self.button.configure(state='disabled')
        if state == True and currentstate == 'disabled':
            core.debug(f"Button: enabling button {self.name}")
            self.button.configure(state='normal') # enables button if supplied bool is true

    def clear(self):
        core.debug(f'Button: destroying "{self.name}"')
        self.button.destroy()

    def getsettings(self):
        self.darkaccent = core.settings.darkaccent
        self.highlight = core.settings.highlight
        self.accent = core.settings.accent
        self.background = core.settings.background
        self.border = core.settings.border
        self.text = core.settings.text

class Inputbox:
    def __init__(self, parent, row, name, value, typename, backgroundcolor):
        core.debug(f'InputBox: Creating "{name}" with value: {value}')

        self.name = name
        self.type = typename
        
        self.main = ctk.CTkFrame(parent,
        fg_color=backgroundcolor, # creates the frame
        corner_radius=0)

        self.main.grid(column=0, row=row, sticky='NSEW') # places it in the parent

        self.main.columnconfigure(0, weight=0)
        self.main.columnconfigure(1, weight=1)
        self.main.columnconfigure(2, weight=0)

        self.title = ctk.CTkLabel(self.main, text_color=core.settings.text, fg_color=backgroundcolor,
            text=name)
        self.title.grid(column=0, row=0, sticky='W', padx=4, pady=1)
        
        self.value = tk.StringVar(name=self.name, value=value)

        root = parent.winfo_toplevel()
        checknumber = root.register(self.validvaluecheck)

        self.input = ctk.CTkEntry(self.main, textvariable=self.value, 
                                  validate = 'key',
                                  validatecommand=(checknumber, '%P'),
                                  fg_color=backgroundcolor,
                                  text_color=core.settings.text,
                                  border_color=core.settings.border,
                                  width=150,
                                  height=15,
                                  )
        self.input.grid(column=2, row=0, sticky='E', padx=4, pady=1)
    
    def valuegetupdates(self, enablewrite):
        self.trace = self.value.trace_add('write', enablewrite)

    def valueset(self, oldvalue):
        self.value.set(oldvalue)

    def toggle(self):
        if self.input._state == 'normal':
            self.input.configure(state='disabled')
        else:
            self.input.configure(state='normal')

    def clear(self):
        core.debug(f'InputBox: Destroying {self.name}')
        self.value.trace_remove('write', self.trace)
        self.main.destroy()

    def getvalue(self):
        newval = self.input.get()
        if newval == '':
            return 0
        if self.type == 'float':
            newval = float(newval)
        elif 'int' in self.type:
            newval = int(newval)
        core.debug(f'InputBox: Returning {newval}')
        return newval

    def validvaluecheck(self, typedvalue):
        if typedvalue == "":
            return True
        try:
            if self.type == 'float':
                float(typedvalue)
            else:
                int(typedvalue)
            return True
        except ValueError:
            return False

class Separator:
    def __init__(self, parent, row:int, column:int, span:int, orientation:str):
        if orientation == 'horizontal':
            self.main = ctk.CTkFrame(parent, height=2, fg_color=core.settings.border)
            self.main.grid(row=row, column=column, columnspan=span, sticky='EW')
        elif orientation == 'vertical':
            self.main = ctk.CTkFrame(parent, width=2, fg_color=core.settings.border)
            self.main.grid(row=row, column=column, rowspan=span, sticky='NS')
            
class Dropdown:
    def __init__(self, parent, row, name, value, typename, dictionary, backgroundcolor):
        core.debug(f'Dropdown: Creating "{name}" with value: {value}')

        self.name = name
        self.type = typename
        self.list = dictionary['list']
        self.list_reverse = dictionary['list_reverse']
        self.values = list(self.list.keys())
        self.value = tk.StringVar(name=self.name, value=self.list_reverse[str(value)])
        
        self.main = ctk.CTkFrame(parent,
        fg_color=backgroundcolor, # creates the frame
        corner_radius=0)

        self.main.grid(column=0, row=row, sticky='NSEW') # places it in the parent

        self.main.columnconfigure(0, weight=0)
        self.main.columnconfigure(1, weight=1)
        self.main.columnconfigure(2, weight=0)

        self.title = ctk.CTkLabel(self.main, text_color=core.settings.text, fg_color=backgroundcolor,
            text=name)
        self.title.grid(column=0, row=0, sticky='W', padx=4, pady=1)
        
        self.input = ctk.CTkComboBox(self.main, variable=self.value,
                                  values=self.values,
                                  fg_color=backgroundcolor,
                                  text_color=core.settings.text,
                                  border_color=core.settings.border,
                                  width=150,
                                  height=15,
                                  )
        self.input.grid(column=2, row=0, sticky='E', padx=4, pady=1)
    
    def valuegetupdates(self, enablewrite):
        self.trace = self.value.trace_add('write', enablewrite)

    def valueset(self, oldvalue):
        self.value.set(self.list_reverse[str(oldvalue)])

    def toggle(self):
        if self.input._state == 'normal':
            self.input.configure(state='disabled')
        else:
            self.input.configure(state='normal')

    def clear(self):
        core.debug(f'Dropdown: Destroying {self.name}')
        self.value.trace_remove('write', self.trace)
        self.main.destroy()

    def getvalue(self):
        input = self.input.get()
        if input == '':
            return None
        print(input)
        newval = self.list[input]
        print(newval)
        if newval == '':
            return 0
        if self.type == 'float':
            newval = float(newval)
        elif 'int' in self.type:
            newval = int(newval)
        core.debug(f'Dropdown: Returning {newval}')
        return newval



