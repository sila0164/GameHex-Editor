import dearpygui.dearpygui as dpg
from core.common import dev, debug, error
import core.settings as cs
import core.file as cf
import core.buttons as cb

editor_is_built = False

def init(open_function, save_function, save_as_function, undo_function, settings_function, exit_function):
    dpg.create_context()
    dpg.create_viewport(title=cs.settings.language[12])

    if cs.settings.debug == False:
        dpg.set_viewport_height(600)
        dpg.set_viewport_width(600)
    else:
        dpg.set_viewport_height(600)
        dpg.set_viewport_width(700)

    dpg.set_viewport_large_icon("gui/icon.ico")
    dpg.set_viewport_small_icon("gui/icon.ico")

    with dpg.window(label=cs.settings.language[12], tag='Primary', no_scrollbar=True, no_scroll_with_mouse=True):
        with dpg.menu_bar():
            with dpg.menu(label=cs.settings.language[33]): #File menu
                dpg.add_menu_item(tag='open_button', label=cs.settings.language[5], callback=open_function) # Open button for opening files
                dpg.add_menu_item(tag='save_button', label=cs.settings.language[34], callback=save_function, enabled=False) # Save button for saving
                dpg.add_menu_item(tag='saveas_button', label=cs.settings.language[35], callback=save_as_function, enabled=False) # Save As button for saving as
                dpg.add_menu_item(tag='undo_button', label=cs.settings.language[6], callback=undo_function, enabled=False) # Undo button
                dpg.add_menu_item(tag='settings_button', label=cs.settings.language[36], callback=settings_function) # cs.settings button for opening cs.settings
                dpg.add_menu_item(tag='close_button', label=cs.settings.language[0], callback=exit_function) # Exit button for exiting the program
            with dpg.menu(label='|', enabled=False):
                pass
            with dpg.menu(label=cs.settings.language[13], enabled=False, tag='message_display'): # "Message display"
                pass
        #with dpg.child_window(border=False, tag='editor'): # The main editor area
            #pass

    dpg.set_primary_window('Primary', True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()

def change_message(message: int):
    dpg.set_value('message_display', cs.settings.language[message])

def close_main_window():
    dpg.destroy_context()

def build_editor():
    dev('Building editor')
    with dpg.child_window(parent = 'Primary', tag='editor'):
        with dpg.tab_bar(tag='open_files'):
            pass

def add_file_tab(file):
    dev(f'Adding file tab for {file.fullname}')
    with dpg.tab(tag=file.fullname, label=file.fullname, parent='open_files'):
        for id in file.stat:
            if file.stat[id]['hidden'] == True and cs.settings.hidehidden == True:
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
            if file.stat[id]['dict'] != None:
                list = file.stat[id]['dict']['list']
            else:
                list = None
            type = file.stat[id]["type"]
            with dpg.child_window(height=25, border=False, no_scrollbar=True, tag=title):
                with dpg.group(horizontal=True):
                    dpg.add_text(title,) #width=400)
                    if cs.settings.debug == True or cs.settings.devdebug == True:
                        offset = file.stat[id]["offset"]
                        endian = file.stat[id]['endian']
                        dpg.add_text(' - @' + str(offset) + ' ' + cs.settings.language[37] + ' ' + type + ' ' + cs.settings.language[38] + endian + ' endian')
                    if removable == False:
                        width = 200
                        if list == None and 'float' in type:
                            dpg.add_input_float(width=width, default_value=float(value), step=1)
                        elif list == None and 'int' in type:
                            dpg.add_input_int(width=width, default_value=int(value), step=1) # ADD: Value caps for each type
                        elif list != None:
                            dpg.add_combo(items=list.keys())
                    else:
                        width = 150
                        if list == None and 'float' in type:
                            dpg.add_input_float(width=width, default_value=float(value), step=1)
                        elif list == None and 'int' in type:
                            dpg.add_input_int(width=width, default_value=int(value), step=1) # ADD: Value caps for each type
                        elif list != None:
                            dpg.add_combo(items=list.keys())
                        dpg.add_button(label='+', callback=cb.remove)
                        dpg.add_button(label='-', callback=cb.add)
                    
        


            
            

