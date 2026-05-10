import dearpygui.dearpygui as dpg
from core.common import dev, type_max_value, type_min_value


def int_value_validation(sender, app_data, user_data):
    type = user_data[0]
    last_value = user_data[1]
    
    try:
        value = int(app_data)
        if type_min_value[type] <= value <= type_max_value[type]:
            last_value = value
        else:
            dpg.set_value(sender, str(last_value))

    except ValueError:
        dpg.set_value(sender, str(last_value))

def init(open_function, save_function):
    #Creating the window
    debug = True
    print("mainwindow: Creating window")
    title = "GameHex Editor 0.2"
    dpg.create_context()
    dpg.create_viewport(title = title)
    dpg.set_viewport_height(600)
    dpg.set_viewport_width(570)
    if debug == True:
        dpg.set_viewport_width(800)
    dpg.set_viewport_large_icon("gui/icon.ico")
    dpg.set_viewport_small_icon("gui/icon.ico")


    with dpg.window(label=title, tag='editor', no_scrollbar=True, no_scroll_with_mouse=True):
        with dpg.menu_bar():
            with dpg.menu(label="File"): #File menu
                dpg.add_menu_item(tag='open_button', label="Open", callback=open_function) # Open button for opening files
                dpg.add_menu_item(tag='save_button', label="Write to file", callback=save_function, enabled=False) # Save button for saving
                #dpg.add_menu_item(tag='saveas_button', label=cs.settings.language[35], callback=save_as_function, enabled=False) # Save As button for saving as
                #dpg.add_menu_item(tag='undo_button', label=cs.settings.language[6], callback=undo_function, enabled=False) # Undo button
                #dpg.add_menu_item(tag='settings_button', label=cs.settings.language[36], callback=settings_function) # cs.settings button for opening cs.settings
                #dpg.add_menu_item(tag='close_button', label="Close Program", callback=close_main_window()) # Exit button for exiting the program

    dpg.set_primary_window('editor', True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()

def create_table(parent: str, name: str):
    debug = True
    #Creates a table to contain all the data
    with dpg.table(header_row=False, 
                    borders_innerH=True, 
                    borders_outerH=True, 
                    borders_innerV=True, 
                    borders_outerV=True,
                    tag=name,
                    parent=parent):
        dpg.add_table_column(width_stretch=True)
        #One column to contain the extra debug info
        if debug == True:
            dpg.add_table_column(width_fixed=True, init_width_or_weight=230)
        dpg.add_table_column(width_fixed=True, init_width_or_weight=150)

def load_file_to_ui(file, hidehidden: bool = False, debug: bool = False):

    debug = True
    hidehidden = True

    print(f'MainUI: Opening file')
    with dpg.group(parent='editor',
                   tag='main'):
        pass        

    create_table(parent='main', name='default')

    for id in file.stat:

        # Hides the value if hidehidden is false
        if file.stat[id]['hidden'] == True and hidehidden == True:
            print(f'Skipping {file.stat[id]["title"]}, value is hidden')
            continue

        # Gets the ui title for the value
        title = file.stat[id]['title']

        # newvalue is a value given in the script to overwrite the actual value in the file
        newvalue = file.stat[id]['newvalue']
        if newvalue == None:
            value = file.stat[id]['value']
        else:
            value = newvalue

        # removable and addable are bools that allow removing or adding the data entirely from the file
        removable = file.stat[id]['removable']
        addable = file.stat[id]['addable']
        
        # If the data is from a list, get the list and make it as a dropdown
        if file.stat[id]['dict'] != None:
            items_list = file.stat[id]['dict']['list']
            items_list_reverse = file.stat[id]['dict']['list_reverse']
        else:
            items_list = None
        
        #gets the data type for the value
        type = file.stat[id]["type"]

        #Creates a new row in the parent
        with dpg.table_row(parent='default'):

            # Adds the header text.    
            dpg.add_text(title)

            # If debug is enabled show extra details about a given value
            if debug == True:
                offset = file.stat[id]["offset"]
                endian = file.stat[id]['endian']
                dpg.add_text('@' + str(offset) + ' as ' + type + ' in ' + endian + ' endian')

            # Adds the correct input depending on value type
            if items_list == None and 'float' in type:
                dpg.add_input_float(default_value=float(value),
                                    step=0, 
                                    tag=id,
                                    width=150)
            elif items_list == None and 'int' in type:
                dpg.add_input_text(default_value=str(value),  
                                    tag=id,
                                    decimal=True,
                                    callback=int_value_validation,
                                    user_data=[type, value],
                                    width=150)
            elif items_list != None:
                dpg.add_combo(items=list(items_list.keys()),
                                tag=id,
                                width=150,
                                default_value=items_list_reverse[value])
            else:
                print(f'Unsupported type {type} for {title}')

    # Enables the save button after loading a file
    dpg.configure_item(item='save_button', enabled=True) 
                     
def write_file_from_ui(file):
    new_values = {}
    for id in file.stat:
        new_value = dpg.get_value(id)
        new_values[id] = new_value
    file.write(new_values)
        
def reset_editor():
    dev('File is open, resetting editor')
    dpg.delete_item('main')
            

