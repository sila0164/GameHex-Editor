import core.settings as cs
from tkinter import filedialog
from gui import * 
import core.file as file
from core.file import File

class Main:
    def __init__(self):
        # creates main window
        print('\nMain: Creating window')
        self.window = MainWindow()
        self.root = self.window.root
        self.buttonbox = ButtonBox(self.window.main)
        self.filedisplay = FileDisplay(13, self.window.main)
        self.statdisplay = StatDisplay(self.window.main)
        #Buttons for buttonbox
        self.open = Button(self.buttonbox.main, 5, self.openfile)
        self.buttonbox.placebutton(self.open.button)
        self.buttonbox.space()
        self.write = Button(self.buttonbox.main, 18, self.writetofile, state=False)
        self.buttonbox.placebutton(self.write.button)
        self.buttonbox.space()
        self.revert = Button(self.buttonbox.main, 6, self.revertstats, state=False)
        self.buttonbox.placebutton(self.revert.button)
        self.revertoriginal = Button(self.buttonbox.main, 16, self.revertoriginalstats, state=False)
        self.buttonbox.placebutton(self.revertoriginal.button)
        self.exit = Button(self.buttonbox.main, 0, self.exitprogram)
        self.buttonbox.placebutton(self.exit.button, lastbutton=True)

        self.firstopen = True
        self.newfile = False
        self.filehasbeenedited = False 

        self.root.mainloop()

    def updatebuttons(self, varname, index, mode):
        print(f'Main: {varname} was changed')
        if self.newfile == False:
            self.statdisplay.updaterevert(varname)
            self.filehasbeenedited = True
            self.write.changestate()
            if self.statdisplay.revertcount > 0:
                self.revertoriginal.changestate()
                self.revert.changestate()
        else:
            self.write.changestate(False)
            self.revertoriginal.changestate(False)
            self.revert.changestate(False)
        self.newfile = False

    def openfile(self):
        print('Main: User pressed Open')
        tempfilepath = None
        savefilereminder = True
        if self.filehasbeenedited == True:
            print('Main: Unwritten changes, opening prompt')
            savefilereminder = self.filealreadyopencheck() # prompts the user if they want to save first. Gets False if they cancel

        if savefilereminder == True:
            tempfilepath = filedialog.askopenfilename(title="Open a File")

        if tempfilepath: # If the user selected a file continue
            print('Main: File selected - Checking Support')
            self.filedisplay.changetext(17)
            tempfile = File(tempfilepath) # creates the openend file as a fileclass
            self.supportcheck(tempfile) # Function that checks whether a file is supported

    def filealreadyopencheck(self) -> bool:
        print('Main: Checking no file is already open')
        continueload = True
        if file.current != None:
            popup = Popup(23, 24, root=self.root)
            continueload = popup.buttonsbool(25, 26)   
        return continueload
    
    def supportcheck(self, tempfile):
        continueload = False
        support = tempfile.hassupport() # returns a string depending on support-level; confirmed, unknown, unsupported
        if support == 'confirmed': # if the id is known, it will just read it
            print('Main: Support check: Full Support')
            continueload = True
        if support == 'unknown': # if the file extension is known, but the id isnt, the user is prompted to choose whether or not to continue
            print('Main: Support check: Fileextension Support, unknown ID.')
            popup = Popup(7, 8, root=self.root)
            continueload = popup.buttonsbool(9,10)
        if support == 'unsupported': # Informs the user the file isnt supported and doesnt continue
            print('Main: Support check: Unsupported')
            popup = Popup(11, 14, root=self.root)
            popup.buttonsackknowledge(15)
            if self.firstopen == True:
                self.filedisplay.changetext(13)
            else:
                self.filedisplay.changetext(file.current.fullname)
        if continueload == True:
            print('Main: Mounting file')
            tempfile.mount() # Mounts the file as core.file.current
            #searchpattern = settings.searchpatterns[file.current.extension] # figures out what searchpattern to use
            #searchpattern() # runs the searchpattern
            print('\n----------------------------------------------------------------------------------')
            print(f'\nMain: {file.current.fullname}\n')
            print('----------------------------------------------------------------------------------\n')
            from Suites.GhostReconBreakpoint.GR_WeaponDBEntry import read as readweaponentry
            readweaponentry()
            if self.firstopen == False:
                print('Main: Clearing statdisplay, already had file loaded')
                self.statdisplay.clear()
            self.firstopen = False
            self.statdisplay.newfile(self.updatebuttons)
            self.filedisplay.changetext(file.current.fullname)
            self.newfile = True

    def disableallbuttons(self):
        print('Main: Disabling all buttons')
        self.write.changestate(False)
        self.open.changestate(False)
        self.exit.changestate(False)
        self.revert.changestate(False)
        self.revertoriginal.changestate(False)
    
    def enableallbuttons(self):
        print('Main: Enabling all buttons')
        self.write.changestate(True)
        self.open.changestate(True)
        self.exit.changestate(True)
        self.revert.changestate(True)
        self.revertoriginal.changestate(True)

    def writetofile(self):
        print('Main: Writing to file')
        self.disableallbuttons()
        self.statdisplay.state_toggleall()
        self.filedisplay.changetext(19)
        writeok = self.statdisplay.sendnewvaluestofile()
        if writeok == True:
            file.current.write()
            self.filedisplay.changetext(20, file.current.fullname)
            self.filehasbeenedited = False
            self.enableallbuttons()
            if self.statdisplay.revertcount <= 0:
                self.revertoriginal.changestate(False)
                self.revert.changestate(False)
            self.write.changestate(False)
            print('Main: Write OK!')
        else:
            print('Main: Something went wrong when writing')
            popup = Popup(22, 21, self.root)
            popup.buttonsackknowledge(15)
            self.filedisplay.changetext(file.current.fullname)
            self.enableallbuttons()
        self.statdisplay.state_toggleall()
        
    def revertstats(self):
        if file.current != None and self.revert:
            print('Main: Reverting last')
            self.revert.changestate(False)
            self.statdisplay.revertlast()
        else:
            print('Main: No file mounted, could not revert.')
        if self.statdisplay.revertcount == 0:
            self.revert.changestate(False)
            self.revertoriginal.changestate(False)
            if file.current.hasbeenwritten == False:
                self.write.changestate(False)
            else:
                self.write.changestate(True)

    def revertoriginalstats(self):
        if file.current != None and self.revertoriginal:
            print('Main: Reverting settings to original')
            self.statdisplay.revertoriginal()
            self.revertoriginal.changestate(False)
            if file.current.hasbeenwritten == False:
                self.write.changestate(False)
        else:
            print('Main: No file mounted, could not revert to original.')

    def exitprogram(self):
        print('Main: Exiting program')
        self.window.exit()
        

if __name__ == '__main__': 
    settingsinit = cs.initsettings()
    if settingsinit == False: # stops the program if settings couldnt be set
        popup = Popup(1, 8, backup=True) # Creates a popup telling the user settings are broke
        createnewsettings = popup.buttonsbool(9, 10) # asks whether or not a new settings file should be created
        if createnewsettings == True:
            settingsinit = cs.forcecreatesettings()
    # if settings are read properly, imports everything and starts Main(controller)
    if settingsinit == True:
        Main()
