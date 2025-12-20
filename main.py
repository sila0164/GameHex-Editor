import core
from tkinter import filedialog
from gui import * 
import time

class Main:
    def __init__(self):
        # creates main window
        print('\nMain: Creating window')
        start = time.time()
        self.window = MainWindow()
        self.root = self.window.root
        self.buttonbox = ButtonBox(self.window.main)
        self.filedisplay = FileDisplay(13, self.window.main)
        self.statdisplay = StatDisplay(self.window.main)
        #Buttons for buttonbox
        self.open = Button(self.buttonbox.main, 5, self.openfile, slim=True)
        self.buttonbox.placebutton(self.open.button)
        self.buttonbox.space()
        self.write = Button(self.buttonbox.main, 18, self.writetofile, state=False, slim=True)
        self.buttonbox.placebutton(self.write.button)
        self.buttonbox.space()
        self.revert = Button(self.buttonbox.main, 6, self.revertstats, state=False, slim=True)
        self.buttonbox.placebutton(self.revert.button)
        self.exit = Button(self.buttonbox.main, 0, self.exitprogram, slim=True)
        self.buttonbox.placebutton(self.exit.button, lastbutton=True)
        self.window.main.after_idle(self.window.unhide)
        self.firstopen = True
        self.filehasbeenedited = False 
        self.revertisactive = False
        end = time.time()
        print(f'Main: Window done. Time Elapsed: {end - start} seconds')

        self.root.mainloop()

    def updatebuttons(self, id, *args):
        print(f'Main: {id} was changed')
        if self.revertisactive == False:
            self.statdisplay.updaterevertlog(id)
            self.filehasbeenedited = True
            self.write.changestate()
            if self.statdisplay.revertcount > 0:
                core.dev(f'updatebuttons: revertcount is more than 0')
                self.revert.changestate()
        
    def openfile(self):
        print('Main: User pressed Open')
        tempfilepath = None
        savefilereminder = True
        if self.filehasbeenedited == True:
            print('Main: File is open, opening prompt')
            savefilereminder = self.filealreadyopencheck() # prompts the user if they want to save first. Gets False if they cancel

        if savefilereminder == True:
            tempfilepath = filedialog.askopenfilename(title="Open a File")

        if tempfilepath: # If the user selected a file continue
            core.dev('Main: File selected - Checking Support')
            self.time_start = time.time()
            self.filedisplay.changetext(17)
            tempfile = core.File(tempfilepath) # creates the openend file as a file-class
            self.supportcheck(tempfile) # Function that checks whether a file is supported

    def filealreadyopencheck(self) -> bool:
        print('Main: Checking no file is already open')
        continueload = True
        if self.current_file and self.write.button._state == 'normal':
            popup = Popup(23, 24, root=self.root)
            continueload = popup.buttonsbool(25, 26)   
        return continueload
    
    def supportcheck(self, tempfile):
        continueload = False
        if tempfile.extension in core.suites.supported_extensions or tempfile.fullname in core.suites.supported_extensions:
            print('Main: Support check: Supported')
            #popup = Popup(7, 8, root=self.root)
            #continueload = popup.buttonsbool(9,10)
            continueload = True
            self.disablebuttons(all=False)
        else:
            print('Main: Support check: Unsupported')
            popup = Popup(11, 14, root=self.root)
            popup.buttonsackknowledge(15)
            if self.firstopen == True:
                self.filedisplay.changetext(13)
            elif self.current_file:
                self.filedisplay.changetext(self.current_file.fullname)
            else:
                core.error('Main: Something went wrong when running supportcheck')
        
        #if support == 'confirmed': # if the id is known, it will just read it
         #   print('Main: Support check: Full Support')
          #  continueload = True
        if continueload == True:
            print('Main: Reading file')
            self.current_file = tempfile
            print('\n----------------------------------------------------------------------------------')
            print(f'\nMain: {self.current_file.fullname}\n')
            print('----------------------------------------------------------------------------------\n')
            core.dev(self.current_file)
            self.script = core.Script(self.current_file, core.suites)
            self.script.run()
            if self.firstopen == False:
                core.dev('Main: Clearing statdisplay, already had file loaded')
                self.statdisplay.clear()
            self.firstopen = False
            self.statdisplay.newfile(self.updatebuttons, self.current_file)
            self.filedisplay.changetext(self.current_file.fullname)
            self.root.after_idle(self.openfilegettime)
            
    def openfilegettime(self):
        self.time_end = time.time()
        print(f'Main: File opened, time elapsed: {self.time_end - self.time_start}')

    def disablebuttons(self, all: bool = True):
        print('Main: Disabling all buttons')
        if all == True:
            self.open.changestate(False)
            self.exit.changestate(False)    
        self.revert.changestate(False)
        self.write.changestate(False)
    
    def enablebuttons(self, write: bool = False):
        print('Main: Enabling all buttons')
        self.write.changestate(write)
        self.open.changestate(True)
        self.exit.changestate(True)
        if self.statdisplay.revertcount > 0:
            self.revert.changestate(True)

    def writetofile(self):
        print('Main: Writing to file')
        self.time_start = time.time()
        if self.current_file == None:
            core.error('Main: Writetofile: File is None')
            return
        self.disablebuttons(all=True)
        self.statdisplay.state_toggleall()
        self.filedisplay.changetext(19)
        new_values =self.statdisplay.getvalue(all=True)
        #try:
        self.current_file.write(new_values)
        writeok = True
        #    except Exception as e:
        #    core.error(f'Main: Something went wrong when writing: {e}')
        #    writeok = False
        if writeok == False:
            popup = Popup(22, 21, self.root)
            popup.buttonsackknowledge(15)
            self.filedisplay.changetext(self.current_file.fullname)
            self.enablebuttons(write=True)

        self.filedisplay.changetext(20, delayedmessage=self.current_file.fullname)
        self.filehasbeenedited = False
        self.enablebuttons(write=False)
        if self.statdisplay.revertcount <= 0:
            self.revert.changestate(False)
        self.write.changestate(False)
        self.statdisplay.state_toggleall()
        self.time_end = time.time()
        print(f'Main: Write done, time elapsed: {self.time_end - self.time_start}')
        
    def revertstats(self):
        print('Main: Reverting last')
        self.revertisactive = True
        self.statdisplay.revertlast()
        if not self.statdisplay.revertcount > 0:
            self.revert.changestate(False)
            if self.current_file.hasbeenwritten == False:
                self.write.changestate(False)
            else:
                self.write.changestate()
        self.revertisactive = False

    def exitprogram(self):
        print('Main: Exiting program')
        savefilereminder = True
        if self.filehasbeenedited == True:
            print('Main: Unwritten changes, opening prompt')
            savefilereminder = self.filealreadyopencheck() # prompts the user if they want to save first. Gets False if they cancel
        if savefilereminder == True:
            self.disablebuttons(all=True)
            self.window.exit()

if __name__ == '__main__': 
    start = time.time()
    print('Main: Initializing settings')
    settings_init = core.initsettings()
    if settings_init == False: # stops the program if settings couldnt be set
        popup = Popup(1, 2) # Creates a popup telling the user settings are broke
        create_new_settings = popup.buttonsbool(9, 10) # asks whether or not a new settings file should be created
        if create_new_settings == True:
            settings_init = core.forcecreatesettings()
    # if settings are read properly, imports everything and starts Main(controller)
    if settings_init == True:
        end = time.time()
        print(f'Main: Settings Initialized. Time elapsed: {end - start} seconds')
        start = time.time()
        suites_ok = core.readsuites()
        end = time.time()
        print(f'Main: Suites Read. Time Elapsed: {end - start} seconds')
        if suites_ok == True:
            Main()
        if suites_ok == False:
            core.error('Main: Something went wrong when loading suites')
