<img width="1305" height="133" alt="Main Banner" src="https://github.com/user-attachments/assets/752f5a03-dc13-42af-be37-f4efa7ee6d1c" />

- # Description:

GameHex is a different take on a hex editor, with a greater focus on ease of use and ui. 

It is primarily meant to help with repetitive tasks, editing many files that have the same layout and sharing knowledge with people who dont know how to use a hex editor.

It was created due to me getting into hex editing encrypted gamefiles, and finding a lack of useful editors for this usecase.

It uses a very simple scripting language, allowing people to create "Suites", for specific games/programs/files.  
You create scripts that the program then ties to an extension or even a full filename, if you need it to be very specific.

When the user then opens a file with an extension the program has a script for, it creates a simple overview of all the read values, which can then be edited and written to the file.  
It can also use lists of known values to create dropdowns.

The program is alpha, not very feature-rich, and it is my first "proper" program. It is currently very specificaly made for what I needed it to do, so I'm sure there's a lot that could be added to make it much more useful for other tasks.  
I imagine Python is a bad/slow choice, but it is what I've ended up learning, and it ultimately works well.

- # Features:

  - A simple clean ui, for easy editing of values
 
  - A simple scripting language to find the values in a file
 
  - Localization support (only english included)
 
  - Reverting changes
 
  - Settings file, where you can change colors
 
  - Expandable Suite system allowing support for an infintie amount of file types


Please include the log, if you report a bug, aswell as a description of what you were trying to do, what you expected to happen and what actually happened.


For an example suite, you can check out my Ghost Recon Breakpoint one on nexus:  
TBD

Documentation for the scripting language:  
https://github.com/sila0164/GameHex-Editor/blob/main/GHEX-Language.md


