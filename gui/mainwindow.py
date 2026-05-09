import dearpygui.dearpygui as dpg



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


    with dpg.window(label=title, tag='Primary', no_scrollbar=True, no_scroll_with_mouse=True):
        with dpg.menu_bar():
            with dpg.menu(label="File"): #File menu
                dpg.add_menu_item(tag='open_button', label="Open", callback=open_function) # Open button for opening files
                dpg.add_menu_item(tag='save_button', label="Write to file", callback=save_function, enabled=False) # Save button for saving
                #dpg.add_menu_item(tag='saveas_button', label=cs.settings.language[35], callback=save_as_function, enabled=False) # Save As button for saving as
                #dpg.add_menu_item(tag='undo_button', label=cs.settings.language[6], callback=undo_function, enabled=False) # Undo button
                #dpg.add_menu_item(tag='settings_button', label=cs.settings.language[36], callback=settings_function) # cs.settings button for opening cs.settings
                #dpg.add_menu_item(tag='close_button', label="Close Program", callback=close_main_window()) # Exit button for exiting the program

    dpg.set_primary_window('Primary', True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()

def load_file_to_ui(file, hidehidden: bool = False, debug: bool = False):

    debug = True

    print(f'Opening file')
    with dpg.group(parent='Primary'):    
        with dpg.table(header_row=False, 
                       borders_innerH=True, 
                       borders_outerH=True, 
                       borders_innerV=True, 
                       borders_outerV=True):
            dpg.add_table_column(width_stretch=True)
            if debug == True:
                dpg.add_table_column(width_fixed=True, init_width_or_weight=230)
            dpg.add_table_column(width_fixed=True, init_width_or_weight=150)
            for id in file.stat:
                if file.stat[id]['hidden'] == True and hidehidden == True:
                    print(f'Skipping {file.stat[id]["title"]}, value is hidden')
                    continue
                title = file.stat[id]['title']
                newvalue = file.stat[id]['newvalue']
                if newvalue == None:
                    value = file.stat[id]['value']
                else:
                    value = newvalue
                removable = file.stat[id]['removable']
                if file.stat[id]['dict'] != None:
                    list = file.stat[id]['dict']['list']
                else:
                    list = None
                type = file.stat[id]["type"]
        
                with dpg.table_row():
                    with dpg.group(horizontal=True):    
                        dpg.add_text(title)
                    if debug == True:
                        offset = file.stat[id]["offset"]
                        endian = file.stat[id]['endian']
                        dpg.add_text('@' + str(offset) + ' as ' + type + ' in ' + endian + ' endian')
                    #if removable == False:
                    width = 150
                    if list == None and 'float' in type:
                        dpg.add_input_float(width=width, 
                                            default_value=float(value), 
                                            step=1, 
                                            tag=id,
                                            )
                    elif list == None and 'int' in type:
                        dpg.add_input_int(width=width, 
                                            default_value=int(value), 
                                            step=1, 
                                            tag=id,
                                            ) # ADD: Value caps for each type
                    elif list != None:
                        dpg.add_combo(items=list.keys,
                                        tag=id,
                                        )
                    else:
                        print(f'Unsupported type {type} for {title}')
    dpg.configure_item(item='save_button', enabled=True) # Enables the save button after loading a file
                        
def write_file_from_ui(file):
    new_values = {}
    for id in file.stat:
        new_value = dpg.get_value(id)
        new_values[id] = new_value
    file.write(new_values)
        

            
            

