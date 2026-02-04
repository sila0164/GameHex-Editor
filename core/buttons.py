from tkinter import filedialog
import core.file as cf
import core.common as cc
import core.settings as cs
import core.ghex as ghex
import dearpygui.dearpygui as dpg

def open():
    filepath = filedialog.askopenfilename()
    if filepath != '':
        tempfile = cf.File(filepath)
    supported = cc.support_check(tempfile, ghex.suites)
    if supported == False:
        dpg.configure_item(item='message_display', label=cs.settings.language[11])
        return
    cf.current_file = tempfile
    dpg.configure_item(item='save_button', enabled=True)
    dpg.configure_item(item='saveas_button', enabled=True)
    dpg.configure_item(item='undo_button', enabled=True)
    ghex.run_script()

def save():
    #cf.current_file.save()
    pass

def saveas():
    pass

def undo():
    pass

def settings():
    pass

def exit():
    pass

def add():
    pass

def remove():
    pass
