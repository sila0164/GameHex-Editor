import dearpygui.dearpygui as dpg
import core
from core import debug, dev

def init(open_function, save_function, save_as_function, undo_function, settings_function, exit_function):
    dpg.create_context()
    dpg.create_viewport(title=core.settings.language[12])

    if core.settings.debug == False:
        dpg.set_viewport_height(600)
        dpg.set_viewport_width(600)
    else:
        dpg.set_viewport_height(600)
        dpg.set_viewport_width(700)

    dpg.set_viewport_large_icon("gui/icon.ico")
    dpg.set_viewport_small_icon("gui/icon.ico")

    with dpg.window(label=core.settings.language[12]):
        with dpg.child_window(height=25, border=False, no_scrollbar=True):
            with dpg.menu_bar():
                with dpg.menu(label=core.settings.language[33]): #File menu
                    dpg.add_menu_item(label=core.settings.language[5], callback=open_function) # Open button for opening files
                    dpg.add_menu_item(label=core.settings.language[34], callback=save_function) # Save button for saving
                    dpg.add_menu_item(label=core.settings.language[35], callback=save_as_function) # Save As button for saving as
                    dpg.add_menu_item(label=core.settings.language[6], callback=undo_function) # Undo button
                    dpg.add_menu_item(label=core.settings.language[36], callback=settings_function) # Settings button for opening settings
                    dpg.add_menu_item(label=core.settings.language[0], callback=exit_function) # Exit button for exiting the program
            dpg.add_separator()
        with dpg.child_window(border=False, tag='editor'): # The main editor area
            with dpg.tab_bar(tag='open_files'):
                pass
        with dpg.child_window(height=25, border=False, no_scrollbar=True, tag='process_bar'): # A process bar, for giving messages and showing progress
            dpg.add_separator()
            dpg.add_text(core.settings.language[13], tag='message_display') # The main message display

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()

def change_message(message: int):
    dev('Main window: Changing message display to: ' + core.settings.language[message])
    dpg.set_value('message_display', core.settings.language[message])

def close_main_window():
    dev('Main window: Closing main window')
    dpg.destroy_context()

def add_file_tab(file:core.File, remove_function, add_function):
    with dpg.tab(tag=file.fullname, label=file.fullname, parent='open_files'):
        #with dpg.tab_bar(tag=file.nodes[0]): This is for later when tabs are added to help organize.
         #   for node in file.nodes:
          #      with dpg.tab(tag=node, label=node):
           #         pass
        for id in file.stat:
            if file.stat[id]['hidden'] == True and core.settings.hidehidden == True:
                debug(f'Skipping {file.stat[id]["title"]}, value is hidden')
                continue
            parent = file.stat[id]['parent']
            title = file.stat[id]['title']
            newvalue = file.stat[id]['newvalue']
            if newvalue == None:
                value = file.stat[id]['value']
            else:
                value = newvalue
            removable = file.stat[id]['removable']
            dict = file.stat[id]['dict']
            type = file.stat[id]["type"]
            with dpg.child_window(height=25, border=False, no_scrollbar=True, tag=title):
                with dpg.group(horizontal=True):
                    dpg.add_text(title, width=400)
                    if core.settings.debug == True or core.settings.devdebug == True:
                        offset = file.stat[id]["offset"]
                        endian = file.stat[id]['endian']
                        dpg.add_text('@ ' + offset + ' ' + core.settings.language[37] + ' ' + type + ' ' + core.settings.language[38] + endian, width=100)
                    if removable == False:
                        width = 200
                        if dict == None and 'float' in type:
                            dpg.add_input_float(width=width, default_value=value, step=1)
                        elif dict == None and 'int' in type:
                            dpg.add_input_int(width=width, default_value=value, step=1) # ADD: Value caps for each type
                        elif dict == True:
                            dpg.add_combo(items=list(dict['list'].keys()))
                    else:
                        width = 150
                        if dict == None and 'float' in type:
                            dpg.add_input_float(width=width, default_value=value, step=1)
                        elif dict == None and 'int' in type:
                            dpg.add_input_int(width=width, default_value=value, step=1) # ADD: Value caps for each type
                        elif dict == True:
                            dpg.add_combo(items=list(dict['list'].keys()))
                        dpg.add_button(label='+', callback=remove_function)
                        dpg.add_button(label='-', callback=add_function)
                    


        
                

class StatDisplay: # The main data manipulation interface
    def __init__(self, parent: ctk.CTkFrame, parentcolumn: int=2, parentrow: int=2):
        if core.settings.treeview != True:
            self.main = ctk.CTkScrollableFrame(parent,
            fg_color=core.settings.darkaccent,
            scrollbar_fg_color=core.settings.background,
            corner_radius=0)
            self.main.grid(row=parentrow, column=parentcolumn, sticky='NSEW')
            self.main.columnconfigure(0, weight=1)
            self.main.columnconfigure(1, weight=0)
        else:
            columns = ['Value', 'Change']
            if core.settings.debug == True:
                columns = ['Offset', 'Value', 'Change']
            self.main = ttk.Treeview(parent,
                                     columns = columns,
                                     padding = 5,)
            self.main.grid(row=parentrow, column=parentcolumn, sticky='NSEW')
            self.main.heading("#0", text="Name")
            self.main.heading("Value", text="Value")
            self.main.heading("Change", text="Change")
            if core.settings.debug == True:
                self.main.heading("Offset", text="Offset") 
        self.revertlastisactive = False
        self.revertoriginalisactive = False
        self.hidehidden = True
    
    def newfile(self, enablewrite, file: core.File):
        dev('StatDiplay: Creating entries')
        self.file = file
        self.traceback = enablewrite
        self.rowcount = 0
        self.revert = {}
        self.revertcount = 0
        self.inputs = {} # keeps track of the inputboxes
        self.inputamount = 0
        if core.settings.treeview != True:
            self.main.grid_remove()
            self.build_editor()
        else:
            self.build_treeview()

    def build_editor(self):
        self.separators = {}
        for id in self.file.stat: # creates an inputbox for each stat in the dictionary
            if self.file.stat[id]['hidden'] == True and self.hidehidden == True:
                debug(f'Hiding {self.file.stat[id]['title']}')
                continue
            self.main.rowconfigure(self.rowcount, weight=0) #Configures the row
            value = self.file.stat[id]['value']
            if self.file.stat[id]["newvalue"] != None:
                value = self.file.stat[id]['newvalue']
            title = self.file.stat[id]['title']
            type = self.file.stat[id]['type']
            offset = self.file.stat[id]['offset']
            bgcolor = core.settings.accent
            colorcalc = self.rowcount / 2
            if colorcalc % 2 == 0: # Makes the backgroundcolor change for every other entry
                bgcolor = core.settings.darkaccent
            if self.file.stat[id]['dict'] != None:
                dictionary = self.file.stat[id]['dict']
                self.inputs[id] = gui.Dropdown(self.main, self.rowcount, title, id, value, type, offset, dictionary, backgroundcolor=bgcolor)
            else:
                self.inputs[id] = gui.Inputbox(self.main, self.rowcount, title, id, value, type, offset, bgcolor)
            self.inputs[id].valuegetupdates(self.traceback)
            self.rowcount += 1 # Counts the row up 1
            self.separators[self.rowcount] = gui.Separator(self.main, self.rowcount, 0, 2, 'horizontal')
            self.rowcount += 1
        self.main.after_idle(self.unhideinputs)

    def build_treeview(self):
        for id in self.file.stat: # creates an inputbox for each stat in the dictionary
            if self.file.stat[id]['hidden'] == True and self.hidehidden == True:
                debug(f'Hiding {self.file.stat[id]['title']}')
                continue
            value = self.file.stat[id]['value']
            if self.file.stat[id]["newvalue"] != None:
                value = self.file.stat[id]['newvalue']
            title = self.file.stat[id]['title']
            type = self.file.stat[id]['type']
            offset = self.file.stat[id]['offset']
            parent = self.file.stat[id]['parent']
            bgcolor = core.settings.accent
            colorcalc = self.rowcount / 2
            if colorcalc % 2 == 0: # Makes the backgroundcolor change for every other entry
                bgcolor = core.settings.darkaccent
            values = [value, 'Change']
            if core.settings.debug == True:
                values = [offset, value, 'Change']
            print(parent)
            print(title, values)
            self.inputs[id] = self.main.insert(parent, 'end', text=title, values=values)
        
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

    def togglehiddenvalues(self):
        if self.hidehidden == True:
            self.hidehidden = False
        elif self.hidehidden == False:
            self.hidehidden = True
        self.clear()
        self.build_editor()

    def clear(self):
        dev('StatDisplay: Clearing')
        self.main.grid_remove()
        for input in self.inputs:
            self.inputs[input].clear()
        for sep in self.separators:
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


dpg.create_context()
dpg.create_viewport(title='Custom Title', width=600, height=300)

with dpg.window(label="Example Window"):
    dpg.add_text("Hello, world")
    dpg.add_button(label="Save")
    dpg.add_input_text(label="string", default_value="Quick brown fox")
    dpg.add_slider_float(label="float", default_value=0.273, max_value=1)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

        
        


            
            

