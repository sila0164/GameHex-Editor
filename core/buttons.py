from tkinter import filedialog
import core.file as cf

def open():
    filepath = filedialog.askopenfilename()
    if filepath != '':
        cf.current_file = cf.File(filepath)

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

