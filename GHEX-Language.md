# General Info:

All files to be read by GameHex use the extension ".ghex". Any file not called ".ghex" gets ignored.
.ghex files are utf-8 text files, and can be created with any text editor.

The program currently does not have any error reporting through the ui. If you want to create your own scripts or lists, use the log for debugging.

For a practical example, check out my Suite for Ghost Recon Breakpoint here:
TBD

# Overview:

The GHEX "Language" is a very simple programming language, that uses a very simple syntax and it is meant to be very forgiving.  
It is nonetheless a good idea to stick to a system, to avoid making the code hard to read.

Each line is a command. It makes it simple to use, but is ultimately not optimal for very long commands. (This could change in the future)

It is for the most part not case sensitive.

It does for the most part not care were in the line commands are placed.

It currently supports two different file structures:

- Scripts: Files that read through a file.  

- Lists: Files that contain names for values. Used to create dropdowns and/or limit what the user is allowed to input.

# Scripts:

- ## General Info

  In GHEX scripts each line is considered 1 instruction.

  Everything in a line is seperated by spaces (" "), except for the first line.  

  All lines start with "@", except for the first line.    

  You can add as many spaces as you like.  

  The order of commands does not matter.  

  The parameters of commands have to follow the command.  

  Names can be added anywhere on the line.  

  Comments work like comments in python. (described under "comments" below)

- ## File (defining script use)

  `file: fileextension /anotherfileextension /filename.fileextension`

  A script starts with `file:` on the first line, followed by the extension or full filename that this script should be used for:
  `file: txt`  
  This would then be used whenever the program opens a .txt.

  `FILE: .txt` and `File:.txt` in any combination is also acceptable syntax, if you prefer. As long as the `:` is in there it will figure it out.  

  If the script supports multiple extensions or files, these can be seperated by `/`:
  
  `file: txt /docx /py`

  If you only want to apply the script to a specific file, you can write the full filename:

  `file: example1.txt /example2.docx`  

  Any file that has a matching full name will use this script. The script is prioritized over a script that is used just for the extension.  
  This can be useful if you have files that have slight variations. For example:

  Script 1 is for the extension:
  
  `file: txt`
  
  Script 2 is for a .txt file where variables are in a different order, or it has a slight variation:
   
  `file: annoyingfile.txt`

  If you open a file called "annoyingfile.txt" script 2 will be used. Script 1 will be used for any other .txt file.

- # Comments
  
  Uses the same system as Python.

  Anything on a line after a "#" is ignored by the program. For example:

  `code that does something here # Anything I write here the program ignores`

- # Commands

  - ## @ (Moving the offset)

    Only integers/decimals are supported.

    `@`  
    If followed by a command, it will execute the command at the current offset. Does nothing on its own.
    
    `@ +XX`  
    Adds XX to the current offset value.
    
    `@ -XX`  
    Subtracts XX from the current offset value.
    
    `@ XX`  
    Sets the current offset value to XX.

  
    More detailed description:

    You can move the offset by using + or -:

    `@ +20`  
    `@ -20`

    You can move the offset to a specific offset by just writing a number without any + or - in front:

    `@ 20`
  
    With no number after the @ nothing will be changed. (Primarily for use with commands, see below).

    `@`  


  - ## read (Reading a value)

    `read` follows an `@` command at the beginning of the line.  
    Can be combined with `search`.

    `read type`  
    Reads the given offset as type. For supported types, see types.
 
    `read listname`  
    Reads the given offset and finds the value in a list. Creates a dropdown with the values from the list.  
    If the value is not on the list, it will call itself "Unknown".
 
    More detailed description:
  
    A line containing `read` will read the value at a given offset. Expects an `@` command at the beginning of the line. (see above)

    `read` can be used to read the value, which can then be edited, or told to find the value in a list, creating a dropdown with only the values from the list. (see Lists below)

    The syntax for reading a value:

    `@ read uint16`

    This would read an int16 at offset 0. (If it hasnt been moved beforehand)

    The syntax for reading and finding the value in a list:

    `@ +18 read nameoflist`

    This would read the value at offset 18, and look for the value in a given list.  
    The type is defined in the list. (see lists section, for info on lists)

  - ## Naming values
 
    Can be added to any line containing read
 
    `"Name for the UI"`  
    `'Name for the UI'`
 
    The text will be used to define the value in the ui.
 
    Detailed description:

    Any text added to a line, using the `read`-command, within "" or '' will be used as the values name, in the ui:

    `@ 40 read float 'Name that descripes the values function'`

    This can be added anywhere on the line. First, at the end, or in the middle, it doesn't matter.

    Without a name, the program will just name them "*Type* *number*", iterating the number up as it reads the same type.

  - ## search (Searching for values)
 
    `search` follows an `@` command at the beginning of the line.  
    Can be combined with `read`.

    `search type value, value`  
    Looks for the given value as the given type. Only supports Integers as value. For supported types, see Types.  
    Multiple values can be given using ",":
 
    `search listname`  
    Looks for any value in the list, using the lists defined type. (see Lists)
 
    `-search xyz`  
    Searches backwards/reverse from the starting point.
 
    `cap value`  
    Caps the search to value. The search will stop at offset + cap. Only supports Integers.
 
    Examples:
    
    The search function can be used to find values:

    `@ -20 search uint32 124981`

    Or to find one of a set of values from a list:

    `@ search nameoflist`

    You can search backwards by using `-search`.
 
    Searches can be capped using `cap XXX` anywhere on the line.  
    This will stop the search at "XXX" from the start point.

    Search and read can be combined on a line like this:

    `@ 40 search mylist read mylist 'This value is a dropdown now'`  
    `@ 60 search mylist "The name can also be here" read uint16 cap 400`  
    `"Or here" @ 80 read mylist -search uint8 200`  

# Lists:

  Lists are used to create dropdowns, to limit the users ability to type in incorrect or corrupt values, or to select a known value.

  `list: nameoflist`  
  A list starts with `list:` on the first line, followed by the name of the list.  
  This name is what you use to refer to it in scripts.  
  The name CANNOT contain spaces.
  
  `TYPE: type`  
  TYPE Defines what type the values of the list are. See below for supported types.
  TYPE Is case sensitive, and has to be all-caps.
  
  `Name For UI: value`  
  Every entry is structured "name of value: value". The name is shown in the dropdown. The value of the selected name will be written to the file.
  
# Types:

  Currently supported types (Alpha 0.1):
  
  unsigned int 8-64 syntax:  
    uint8  
    uint16  
    uint24  
    uint32  
    uint40  
    uint48  
    uint56  
    uint64  

  float syntax:  
    float  
  
