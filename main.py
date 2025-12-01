from core import initsettings
from tkinter import filedialog


class Main:
    def __init__(self):
        # creates main window
        self.window = MainWindow()
        self.buttonbox = ButtonBox(self.window.main)
        self.filedisplay = FileDisplay(13, self.window.main)
        # Adds the buttons
        self.open = Button(self.buttonbox.main, 5, self.openfile)
        self.buttonbox.placebutton(self.open.button)
        self.revert = Button(self.buttonbox.main, 6, self.revertstats, state=False)
        self.buttonbox.placebutton(self.revert.button)
        self.revertoriginal = Button(self.buttonbox.main, 16, self.revertoriginalstats, state=False)
        self.buttonbox.placebutton(self.revertoriginal.button)
        #self.write = self.buttonbox.addbutton('write', self.write, state='false', row=9)
        self.exit = Button(self.buttonbox.main, 0, self.exitprogram)
        self.buttonbox.placebutton(self.exit.button, row=10)
        # Makes the window stay as loop
        self.window.root.mainloop()

    def openfile(self):
        print('Opening File')
        tempfilepath = filedialog.askopenfilename(title="Open a File")
        tempfile = File(tempfilepath)
        support = tempfile.hassupport()
        if support == 'confirmed' and self.revertoriginal:
            tempfile.mount()
            self.revertoriginal.changestate()
        if support == 'unknown':
            popup = Popup(7, 8, root=self.window.root)
            continueload = popup.buttonsbool(9,10)
            if continueload == True and self.revertoriginal:
                tempfile.mount()
                self.revertoriginal.changestate()
        if support == 'unsupported':
            popup = Popup(11, 14, root=self.window.root)
            popup.buttonsackknowledge(15)

    def revertstats(self):
        if file.current != None and self.revert:
            print('Reverting settings')
            file.current.revert()
            self.revert.changestate(False)
        else:
            print('No file mounted, could not revert.')
    
    def revertoriginalstats(self):
        if file.current != None:
            print(file.current)
        else:
            print('No file is loaded')

    def exitprogram(self):
        print('Exiting program')
        self.window.exit()
        

if __name__ == '__main__': # Add a 'overwrite current settings' in popup
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
