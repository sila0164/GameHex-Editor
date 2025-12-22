
<img width="1693" height="168" alt="Ghex main banner" src="https://github.com/user-attachments/assets/2336ed58-fe06-4388-962e-97bfbf14860c" />

GameHex is a different take on a hex editor, with a greater focus on ease of use and ui for the user. 

It is primarily meant to help with repetitive tasks, editing many files that have the same layout and sharing knowledge with people who dont know how to use a hex editor.

It was created due to me getting into hex editing encrypted gamefiles, and finding a lack of useful editors for this usecase.

It uses a very simple scripting "language", allowing people to create "Suites", for specific games/programs/files.  
You create scripts that the program then ties to an extension or even a full filename, if you need it to be very specific.

When the user then opens a file with an extension the program has a script for, it creates a simple overview of all the read values, which can then be edited and written to the file.  
It can also use lists of known values to create dropdowns.

The program is alpha, not very feature-rich, and it is my first "proper" program. It is currently very specificaly made for what I needed it to do, so I'm sure there's a lot that could be added to make it much more useful for other tasks.  
I imagine Python is a bad/slow choice, but it is what I've ended up learning, and it ultimately works well.

---

<img width="1693" height="168" alt="Ghex features banner" src="https://github.com/user-attachments/assets/1c2facc9-e0a1-45ab-9fbc-0a9ae27c310b" />


  - A simple clean ui, for easy editing of values
 
  - A simple scripting language to find the values in a file
 
  - Localization support (english and danish included)
 
  - Settings file, where you can change colors, language and enable/disable extra info in the log
 
  - Expandable Suite system allowing support for an infinite amount of file types


---

# How to use:

1. Ensure you have a suite that supports the file you want to open.

2. Open the program and press open. NOTE: The program does not backup files. Make sure you have a way to replave the file in case something goes wrong.

3. Select the file and the program will open the file using the script that supports it.

4. Edit the values you want to change. NOTE: The program does not change anything in the file until "write" is pressed. The file is also not open while editing, only when reading and writing occurs.

5. When done, press Write to write the values to the file. When the program says "File written!" at the top, the changes have been written to the file.

6. Rinse and repeat as much as you want!

---

# Reporting Bugs
  
Please include the log, if you report a bug, aswell as a description of what you were trying to do, what you expected to happen and what actually happened.

# Scripting Language Documentation

Documentation for the scripting language:  
https://github.com/sila0164/GameHex-Editor/blob/main/GHEX-Language.md


