import core
import struct
from core import dev
import customtkinter as ctk
import tkinter as tk

class Button:
    def __init__(self, parent, label, function, state:bool = True, slim:bool = False):
        self.getsettings()
        if isinstance(label, int): # If label is a number get it from settings language. If it isnt, its a string from popup and settings is corrupt/None
            label = core.settings.language[label]
        self.name = label
        width = 100
        if slim == True:
            width = 50
        dev(f'Button: Creating "{self.name}" with state: {state}')
        self.button = ctk.CTkButton(parent, text=label, command=function,
        fg_color=self.background, 
        text_color=self.text, 
        border_color=self.border,
        border_width=2,
        corner_radius=5,
        hover_color=self.highlight,
        text_color_disabled=self.darkaccent,
        width=width)
        if state == False:
            self.button.configure(state='disabled')

    def changestate(self, state:bool = True):
        currentstate = self.button._state # Mostly to avoid spam in terminal. Also stops any undesired behaviour in ui
        if state == False and currentstate == 'normal': # disables button if supplied bool is false
            dev(f"Button: disabling button {self.name}")
            self.button.configure(state='disabled')
        if state == True and currentstate == 'disabled':
            dev(f"Button: enabling button {self.name}")
            self.button.configure(state='normal') # enables button if supplied bool is true

    def clear(self):
        dev(f'Button: destroying "{self.name}"')
        self.button.destroy()

    def getsettings(self):
        self.darkaccent = core.settings.darkaccent
        self.highlight = core.settings.highlight
        self.accent = core.settings.accent
        self.background = core.settings.background
        self.border = core.settings.border
        self.text = core.settings.text

class Inputbox:
    def __init__(self, parent, row, title, id, value, typename, offset, backgroundcolor):
        dev(f'InputBox: Creating {id} - "{title}" with value: {value}')
        self.id = id
        self.type = typename
        self.row = row
        
        self.main = ctk.CTkFrame(parent,
        fg_color=backgroundcolor, 
        corner_radius=0)

        self.main.columnconfigure(0, weight=0)
        self.main.columnconfigure(1, weight=1)
        self.main.columnconfigure(2, weight=0)
        if core.settings.debug == True:
            self.debuglabel = ctk.CTkLabel(self.main, 
                                           text_color=core.settings.text, 
                                           fg_color=backgroundcolor,
                                           text=(f'{typename} @{hex(offset)} ({offset})'))
            self.debuglabel.grid(column=1, row=0, sticky='E', padx=4, pady=1)

        self.label = ctk.CTkLabel(self.main, text_color=core.settings.text, fg_color=backgroundcolor,
            text=title)
        
        self.value = tk.StringVar(name=self.id, value=value)
        self.lastvalue = self.value.get()

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
        self.input.bind('<FocusIn>', self.infocus)

    def infocus(self, event=None):
        dev(f'InputBox: {self.id} in focus')
        self.lastvalue = self.value.get()

    def valuegetupdates(self, enablewrite):
        self.traceback = enablewrite
        self.trace = self.value.trace_add('write', self.value_change)

    def value_change(self, *args):
        current_value = self.value.get()
        dev(f'InputBox: {self.id} Value has changed: {current_value}')
        if current_value != self.lastvalue:
            dev(f'Inputbox: {self.id} Running traceback')
            self.traceback(self.id)

    def unhide(self):
        self.main.grid(column=0, row=self.row, sticky='NSEW')
        self.label.grid(column=0, row=0, sticky='W', padx=4, pady=1)
        self.input.grid(column=2, row=0, sticky='E', padx=4, pady=1)

    def valueset(self, value):
        self.value.set(value)

    def toggle(self):
        if self.input._state == 'normal':
            self.input.configure(state='disabled')
        else:
            self.input.configure(state='normal')

    def clear(self):
        dev(f'InputBox: Destroying {self.id}')
        self.value.trace_remove('write', self.trace)
        self.main.destroy()

    def getvalue(self) -> str:
        newval = self.input.get()
        if newval in ('', '-', '-.', '.'):
            return '0'
        dev(f'InputBox: Returning {newval}')
        return newval

    def validvaluecheck(self, typedvalue):
        if typedvalue in ('', '-', '.', '-.'):
            return True
        try:
            if 'float' in self.type:
                value = float(typedvalue)
                return True
            elif 'int' in self.type:
                value = int(typedvalue)
                typelength = core.typelengths[self.type]
                if 'uint' in self.type:
                    value.to_bytes(typelength, byteorder="little", signed=False)
                    return True
                elif 'int' in self.type:
                    value.to_bytes(typelength, byteorder='little', signed=True)
                    return True

            core.error('InputBox: Invalid Type. This shouldnt happen, please report as a bug.')
            return False
        except (ValueError, struct.error, OverflowError):
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
    def __init__(self, parent, row, title, id, value, typename, offset, dictionary, backgroundcolor):
        dev(f'Dropdown: Creating {id} - "{title}" with value: {value}')

        self.id = id
        self.type = typename
        self.list = dictionary['list']
        self.list_reverse = dictionary['list_reverse']
        self.values = list(self.list.keys())
        self.value = tk.StringVar(name=self.id, value=self.list_reverse[str(value)])
        self.lastvalue = self.value.get()
        self.row = row
        
        self.main = ctk.CTkFrame(parent,
        fg_color=backgroundcolor,
        corner_radius=0)

        self.main.columnconfigure(0, weight=0)
        self.main.columnconfigure(1, weight=1)
        self.main.columnconfigure(2, weight=0)
        if core.settings.debug == True:
            self.debuglabel = ctk.CTkLabel(self.main, 
                                           text_color=core.settings.text, 
                                           fg_color=backgroundcolor,
                                           text=(f'{typename} @{hex(offset)} ({offset})'))
            self.debuglabel.grid(column=1, row=0, sticky='E', padx=4, pady=1)

        self.label = ctk.CTkLabel(self.main, text_color=core.settings.text, fg_color=backgroundcolor,
            text=title)
        
        self.input = ctk.CTkComboBox(self.main, variable=self.value,
                                  values=self.values,
                                  fg_color=backgroundcolor,
                                  text_color=core.settings.text,
                                  border_color=core.settings.border,
                                  width=150,
                                  height=15,
                                  )
        self.input.bind('<FocusIn>', self.infocus)

    def infocus(self, event=None):
        dev(f'InputBox: {self.id} in focus')
        self.lastvalue = self.value.get()

    def valuegetupdates(self, enablewrite):
        self.traceback = enablewrite
        self.trace = self.value.trace_add('write', self.value_change)

    def value_change(self, *args):
        current_value = self.value.get()
        dev(f'InputBox: {self.id} Value has changed: {current_value}')
        if current_value != self.lastvalue:
            dev(f'Inputbox: {self.id} Running traceback')
            self.traceback(self.id)

    def unhide(self):
        self.main.grid(column=0, row=self.row, sticky='NSEW')
        self.label.grid(column=0, row=0, sticky='W', padx=4, pady=1)
        self.input.grid(column=2, row=0, sticky='E', padx=4, pady=1)

    def valueset(self, oldvalue):
        self.value.set(self.list_reverse[str(oldvalue)])

    def toggle(self):
        if self.input._state == 'normal':
            self.input.configure(state='disabled')
        else:
            self.input.configure(state='normal')

    def clear(self):
        dev(f'Dropdown: Destroying {self.id}')
        self.value.trace_remove('write', self.trace)
        self.main.destroy()

    def getvalue(self):
        input = self.input.get()
        newval = self.list[input]
        if newval == '':
            return 0
        if self.type == 'float':
            newval = float(newval)
        elif 'int' in self.type:
            newval = int(newval)
        dev(f'Dropdown: Returning {newval}')
        return newval



