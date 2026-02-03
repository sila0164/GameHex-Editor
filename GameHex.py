import time
import core.settings as cs
import core.file as cf
import core.buttons as cb
import gui.mainwindow as mw
import gui.popups as popup
import core.buttons as button


def open_button():
    if cf.current_file != None:
        if cf.current_file.filehasbeenedited == True:
            popup.unsaved_changes()
        else:
            pass
    else:
        cb.open()



if __name__ == '__main__': 
    start = time.time()
    print('Main: Getting settings')
    cs.settings = cs.Settings()
    end = time.time()
    print(f'Main: Settings Initialized. Time elapsed: {end - start} seconds')
    #start = time.time()
    #suites_ok = core.readsuites()
    #end = time.time()
    #print(f'Main: Suites Read. Time Elapsed: {end - start} seconds')
    suites_ok = True
    if suites_ok == True:
        mw.init(button.open, button.save, button.saveas, button.undo, button.settings, button.exit)
    #if suites_ok == False:
    #    core.error('Main: Something went wrong when loading suites')
