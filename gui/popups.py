import dearpygui.dearpygui as dpg
import core.buttons as cb
import core.settings as cs
import core.file as cf

def yes_button_callback(popup_name):
    dpg.delete_item(popup_name)
    cb.save()
    cb.open()

def no_button_callback(popup_name):
    dpg.delete_item(popup_name)
    cb.open()

def cancel_button_callback(popup_name):
    dpg.delete_item(popup_name)

def unsaved_changes():
    with dpg.window(label='Unsaved Changes', modal=True, tag='unsaved_changes_popup', no_title_bar=True, no_resize=True, no_move=True, width=300, height=150):
        dpg.add_text(cs.settings.language[24]) # "You have unsaved changes. Do you want to save before exiting?"
        with dpg.group(horizontal=True):
            dpg.add_button(label=cs.settings.language[9], tag='unsaved_yes_button', callback=lambda: yes_button_callback(popup_name='unsaved_changes_popup')) # "yes"
            dpg.add_button(label=cs.settings.language[10], tag='unsaved_no_button', callback=lambda: no_button_callback(popup_name='unsaved_changes_popup')) # "no"
            dpg.add_button(label=cs.settings.language[26], tag='unsaved_cancel_button', callback=lambda: cancel_button_callback(popup_name='unsaved_changes_popup')) # "cancel"

