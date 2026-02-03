import dearpygui.dearpygui as dpg
from core.common import dev, debug, error
import core.settings as cs

def init(open_function, save_function, save_as_function, undo_function, settings_function, exit_function):
    settings = cs.settings
    dpg.create_context()
    dpg.create_viewport(title=settings.language[12])

    if settings.debug == False:
        dpg.set_viewport_height(600)
        dpg.set_viewport_width(600)
    else:
        dpg.set_viewport_height(600)
        dpg.set_viewport_width(700)

    dpg.set_viewport_large_icon("gui/icon.ico")
    dpg.set_viewport_small_icon("gui/icon.ico")

    with dpg.window(label=settings.language[12], tag='Primary', no_scrollbar=True, no_scroll_with_mouse=True):
        with dpg.menu_bar():
            with dpg.menu(label=settings.language[33]): #File menu
                dpg.add_menu_item(label=settings.language[5], callback=open_function) # Open button for opening files
                dpg.add_menu_item(label=settings.language[34], callback=save_function, enabled=False) # Save button for saving
                dpg.add_menu_item(label=settings.language[35], callback=save_as_function, enabled=False) # Save As button for saving as
                dpg.add_menu_item(label=settings.language[6], callback=undo_function, enabled=False) # Undo button
                dpg.add_menu_item(label=settings.language[36], callback=settings_function) # Settings button for opening settings
                dpg.add_menu_item(label=settings.language[0], callback=exit_function) # Exit button for exiting the program
            with dpg.menu(label='|', enabled=False):
                pass
            with dpg.menu(label=settings.language[13], enabled=False, tag='message_display'): # "Message display"
                pass
        with dpg.child_window(border=False, tag='editor'): # The main editor area
            #with dpg.tab_bar(tag='open_files'):
            pass

    dpg.set_primary_window('Primary', True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()

def change_message(message: int, settings):
    dpg.set_value('message_display', settings.language[message])

def close_main_window():
    dpg.destroy_context()

def add_file_tab(file:core.File, remove_function, add_function, settings):
    with dpg.tab(tag=file.fullname, label=file.fullname, parent='open_files'):
        #with dpg.tab_bar(tag=file.nodes[0]): This is for later when tabs are added to help organize.
         #   for node in file.nodes:
          #      with dpg.tab(tag=node, label=node):
           #         pass
        for id in file.stat:
            if file.stat[id]['hidden'] == True and settings.hidehidden == True:
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
                    if settings.debug == True or settings.devdebug == True:
                        offset = file.stat[id]["offset"]
                        endian = file.stat[id]['endian']
                        dpg.add_text('@ ' + offset + ' ' + settings.language[37] + ' ' + type + ' ' + settings.language[38] + endian, width=100)
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
                    
        


            
            

