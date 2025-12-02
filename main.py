from core import initsettings
from tkinter import filedialog


class Main:
    def __init__(self):
        from core.settings import settings
        self.firstopen = 0
        # creates main window
        self.window = MainWindow()
        self.buttonbox = ButtonBox(self.window.main)
        self.filedisplay = FileDisplay(13, self.window.main)
        self.statdisplay = StatDisplay(self.window.main)
        # Adds the buttons
        self.open = Button(self.buttonbox.main, 5, self.openfile) # opens filedialog and reads the given file
        self.buttonbox.placebutton(self.open.button)
        self.revert = Button(self.buttonbox.main, 6, self.revertstats, state=False) # reverts to last state before last write
        self.buttonbox.placebutton(self.revert.button)
        self.revertoriginal = Button(self.buttonbox.main, 16, self.revertoriginalstats) #state=False) # Is temporarily a print button for testing
        self.buttonbox.placebutton(self.revertoriginal.button)
        self.write = Button(self.buttonbox.main, 18, self.writetofile, state=False)
        self.buttonbox.placebutton(self.write.button)
        self.exit = Button(self.buttonbox.main, 0, self.exitprogram)
        self.buttonbox.placebutton(self.exit.button, row=10)
        # Makes the window stay as loop
        self.window.root.mainloop()

    def openfile(self):
        print('Main: Opening File')
        tempfilepath = filedialog.askopenfilename(title="Open a File")
        if tempfilepath: # If the user selected a file continue
            self.filedisplay.changetext(17)
            tempfile = File(tempfilepath) # creates the openend file as a fileclass
            self.supportcheck(tempfile) # Function that checks whether a file is supported

    def supportcheck(self, tempfile):
        continueload = False
        support = tempfile.hassupport() # returns a string depending on support-level; confirmed, unknown, unsupported
        if support == 'confirmed': # if the id is known, it will just read it
            continueload = True
        if support == 'unknown': # if the file extension is known, but the id isnt, the user is prompted to choose whether or not to continue
            popup = Popup(7, 8, root=self.window.root)
            continueload = popup.buttonsbool(9,10)
        if support == 'unsupported': # Informs the user the file isnt supported and doesnt continue
            popup = Popup(11, 14, root=self.window.root)
            popup.buttonsackknowledge(15)
            self.filedisplay.changetext(13)
        if continueload == True:
            self.firstopen += 1
            self.write.changestate(True)
            tempfile.mount() # Mounts the file as core.file.current
            #searchpattern = settings.searchpatterns[file.current.extension] # figures out what searchpattern to use
            #searchpattern() # runs the searchpattern
            from Suites.GhostReconBreakpoint.GR_WeaponDBEntry import read as readweaponentry
            readweaponentry()
            self.statdisplayinit()

    def writetofile(self):
        print('Main: Writing to file')
        self.filedisplay.changetext(19)
        writeok = self.statdisplay.sendnewvaluestofile()
        if writeok == True:
            file.current.write()
            self.filedisplay.changetext(20, file.current.fullname)
        else:
            popup = Popup(22, 21)
            popup.buttonsackknowledge(15)
            self.filedisplay.changetext(file.current.fullname)
        

    def statdisplayinit(self):
        if self.firstopen > 1:
            print('Main: Clearing statdisplay')
            self.statdisplay.clear()
        self.statdisplay.update()
        self.filedisplay.changetext(file.current.fullname)

    def revertstats(self):
        if file.current != None and self.revert:
            print('Main: Reverting settings')
            file.current.revert()
            self.revert.changestate(False)
        else:
            print('Main: No file mounted, could not revert.')
    
    def revertoriginalstats(self):
        if file.current != None:
            print(file.current)
        else:
            print('Main: No file is loaded')

    def exitprogram(self):
        print('Main: Exiting program')
        self.window.exit()
        

if __name__ == '__main__': 
    settingsinit = initsettings()
    if settingsinit == False: # stops the program if settings couldnt be set
        from gui.popup import Popup
        popup = Popup(1, 2) # Creates a popup telling the user settings are broke
        popup.buttonsackknowledge(0) # closes the program
    else: # if settings are read properly, imports everything and starts Main(controller)
        from gui import * 
        import core.file as file
        from core import *
        Main()
