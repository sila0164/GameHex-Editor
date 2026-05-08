import time
import core.settings as cs
import core.file as cf
import core.buttons as cb
import gui.mainwindow as mw
import gui.popups as popup
import core.ghex as ghex


def open_button():
    if cf.current_file != None:
        #if cf.current_file.filehasbeenedited == True:
        #    popup.unsaved_changes()
        #else:
        pass
    else:
        cb.open()

if __name__ == '__main__': 
    start = time.time()
    print('Main: Getting settings')
    end = time.time()
    print(f'Main: Settings Initialized. Time elapsed: {end - start} seconds')
    mw.init(open_button, cb.save, cb.saveas, cb.undo, cb.settings, cb.exit)

