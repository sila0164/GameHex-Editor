import time
import core.settings
import gui.mainwindow as mw
import core.buttons as button

if __name__ == '__main__': 
    start = time.time()
    print('Main: Getting settings')
    settings = core.settings.Settings()
    end = time.time()
    print(f'Main: Settings Initialized. Time elapsed: {end - start} seconds')
    #start = time.time()
    #suites_ok = core.readsuites()
    #end = time.time()
    #print(f'Main: Suites Read. Time Elapsed: {end - start} seconds')
    suites_ok = True
    if suites_ok == True:
        mw.init(button.open, button.save, button.saveas, button.undo, button.settings, button.exit, settings)
    #if suites_ok == False:
    #    core.error('Main: Something went wrong when loading suites')
