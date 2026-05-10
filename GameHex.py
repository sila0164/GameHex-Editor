import gui.mainwindow as mw
from tkinter import filedialog
from core.common import debug, dev, support_check
import core.ghex as ghex
import sys, os
from core.file import File

file = None
suites = None

def get_dir() -> tuple[bool, str, str, str | None]:
    is_exe = getattr(sys, 'frozen', False) # Check to see if is running as exe or script

    if is_exe == True: # Sets root of program as either exe or script
        root = os.path.dirname(sys.executable)
    else:
        root = os.path.dirname(os.path.abspath(__file__))

    dev(f'Root: {root}') 
    
    os.chdir(root)  
    sys.path.append(root)

    if is_exe == True:
        sys.stdout = open("Log.txt", "w", encoding="utf-8") # Log file creation, if exe
        log = os.path.join(root, "Log.txt")
    else:
        log = None

    suitesfolder = os.path.join(root, 'SUITES') # Checks for suites folder and creates it if it doesnt exist
    if not os.path.exists(suitesfolder):
        os.makedirs(suitesfolder, exist_ok=False)

    return is_exe, root, suitesfolder, log

def open_button():
    filepath = filedialog.askopenfilename()
    if filepath != '':
        tempfile = File(filepath)
        print(f'\n\n---------\n\nSelected file: {tempfile.fullname}\n\n')
    else:
        print('No file selected')
        return
    global suites
    supported = support_check(tempfile, suites)
    if supported == False:
        #dpg.configure_item(item='message_display', label=cs.settings.language[11])
        print(f'File {tempfile} is not supported')
        return
    script = ghex.Script(tempfile, suites)
    global file
    if file != None:
        mw.reset_editor() # Removes the data from a loaded file, if any
    success, file = script.run() # Runs the script defined for the file
    mw.load_file_to_ui(file) # Loads the read data from the file to the ui


def save_button():
    mw.write_file_from_ui(file)

if __name__ == '__main__': 
    #global is_exe, root, suites_folder, log, suites
    is_exe, root, suites_folder, log = get_dir()
    suites = ghex.Suites(suites_folder)
    mw.init(open_button, save_button)

