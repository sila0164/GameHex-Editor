import os
import sys
from tkinter import ttk
from tkinter import *
import func
from gui import mainwindow, mainwindowinit, filedisplayinit, filedisplay, bottomseparatorinit

#Log file creation:
#sys.stdout = open("Log.txt", "w", encoding="utf-8")

func.statdict = {}
func.stattemp = {}
func.filename = None
func.filepath = None
func.fileu64 = None
func.filetype = None

#Mount current folder as project root:
project_root = os.path.dirname(sys.executable)
os.chdir(project_root)          
sys.path.append(project_root)
func.projectfolder = project_root


#Splash window with open button, to browse for file
mainwindowinit()
filedisplayinit()
filedisplay("Please open a file", "center")
bottomseparatorinit()
mainwindow(buttonsbottom=("empty", "open", "empty",))

func.root.mainloop()