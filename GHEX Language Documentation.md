# General Info:

All files to be read by GameHex use the extension ".ghex". Any file not called ".ghex" gets ignored.
.ghex files are utf-8 text files, and can be created with any text editor.

The program currently does not have any error reporting through the ui. If you want to create your own scripts or lists, use the log for debugging.  
Enabling debug can also be very useful for debugging scripts. Set it to true in Settings.json. Debug prints a lot more info to the log. Debug mode also shows the offset and type of each value in the ui.  
Enabling devdebug adds a lot of clutter to the log and is there to help debug the program, not scripts.  

You still need a hex editor like hxd to find the values.

For a practical example, check out my Suite for Ghost Recon Breakpoint here:
TBD

# Overview:

The GHEX "Language" is a very simple programming language, that uses a very simple linebased, keyword system. It is meant to be easy to use and very forgiving.  
It is nonetheless a good idea to stick to a system, to avoid making the code hard to read.

Each line is a command. It makes it simple to use, but is ultimately not optimal for very long commands. (This could change in the future)

It is for the most part not case sensitive.

It does for the most part not care were in the line commands are placed.

It currently supports two different file structures:

- Scripts: Files that read through a file.  

- Lists: Files that contain names for values. Used to create dropdowns to limit what the user is allowed to input.

# Scripts:

- ## General Info

  In GHEX scripts each line is considered 1 instruction.

  Everything in a line is seperated by spaces (" "), except for the first line.      

  You can add as many spaces as you like.  

  The order of commands does not matter.  

  The parameters of commands have to follow the command.

  Supports both values in decimal and hex. Hex values needs the prefix 'x' or '0x'.

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
  

- # endian (Changing the endian)

  All scripts default to little endian. You can change it using the following command:

  `endian little`  
  `endian big`  

  The command endian can be added anywhere on a line containing other commands to change it for just that command, or be added to a line on its own to change the endian for all the following commands. Has to be followed by either `little` or `big`
  

- # Commands

  - ## @ (Moving the offset)

    `@`  
    If followed by a command, it will execute the command at the current offset. Does nothing on its own.
    Writing `x` or `0x` before the number makes the program read it as a hex value.
    Writing any number with no prefix or hex specific numbers, the program will assume its a decimal/integer.
    
    `@ +XX`  
    Adds XX to the current offset value.
    
    
    `@ -XX`  
    Subtracts XX from the current offset value.
    
    `@ XX`  
    Sets the current offset value to XX.

  
    More detailed description:

    You can move the offset by using + or -:

    `@ +20`
    Adds 20 to the current offset.
     
    `@ -20`
    Subtracts 20 from the current offset.  

    You can move the offset to a specific offset by just writing a number without any + or - in front:

    `@ xA3`
    `@ 0xb2`
    With no prefix the offset will be moved to the given value.
    Writing `x` or `0x` signifies a hex value.  
    
    `@`  
    With no number after the @ nothing will be changed. (Primarily for use with commands, see below).
    

  - ## read (Reading a value)

    `read` follows an `@` command at the beginning of the line.  
    Can be combined with `search`.  
    The offset is automatically moved to after the type, when read. IE if you set an uint64, 8 is added to the current offset.

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
      `'Name for the UI "Using apostrophes allow quotation marks!"'`
 
      The text will be the name used for the value in the ui.
      ' are not supported, and will shorten the name. If you want " in the name use ' to mark the text.
 
      Detailed description:

      Any text added to a line, using the `read`-command, within "" or '' will be used as the values name, in the ui:

      `@ 40 read float 'Name that descripes the values function'`

      This can be added anywhere on the line. First, at the end, or in the middle, it doesn't matter.

      Without a name, the program will just name them "*Type* *number*", iterating the number up as it reads the same type.

    
    - ## removable

      `removable`  
      Adding removable to a read command, makes the value deleteable from the ui.  
      This will delete the bytes in the file. When removed, it can be added it back in again with a button.  

    - ## value (Changing values in the script)
   
      `value XXXX`
      By adding value *value* you can change the value directly from the script.
      The new value will still need to be written, but it will be changed by default in the ui.
      It needs to be a float or integer, depending on what type the value is.

    - ## hidden (Hiding values in ui)
   
      `hidden`
      Makes the value not appear in the ui. It will still be read and changed using the above command. Can be viewed by pressing "show hidden" button.

    - ## node

      `node name_of_node`  
      Adds the read value to a node in the ui. For information about nodes read the nodes section.


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
    If the search is backwards/in reverse the cap has to be negative.
 
    Examples:
    
    The search function can be used to find values:

    `@ -20 search uint32 124981`

    Or to find one of a set of values from a list:

    `@ search name_of_list`

    You can search backwards by using `-search`.
 
    Searches can be capped using `cap XXX` anywhere on the line.  
    This will stop the search at "XXX" from the start point.

    Search and read can be combined on a line like this:

    `@ 40 search mylist read mylist 'This value is a dropdown now'`  
    `@ 60 search mylist "The name can also be here" read uint16 cap 400`  
    `"Or here" @ 80 read mylist -search uint8 200`


  - ## segment (Running a segment/function)

    `@ segment name_of_segment "segment_name_for_ui" removable`
    Will run a segment by the name given. For information on segments read the segments section.  
    Can be named in the ui. This will group every stat from the segment into a treenode.  `
    Can be used with the `removable` command. This will create the segment as a node, with all the values of the segment in it. A removable segment cannot contain search commands.  
    Can be combined with search and repeat in the same line.


  - ## repeat (Repeating a command)
 
    `repeat x`
    `end`
    Will repeat the commands until `end` x times.
    Setting x to -1 will make it repeat until the end of the file.
    
    `search xxxx repeat 5`
    Will repeat a search 5 times.
    A repeated search that goes to the end of a file, will reset to the search's starting offset.

    `search xxxx read xxxx repeat -1`
    Will repeat the search and read until the end of the file is reached.


# Segments:

  Segments are similar to functions in regular programming. It is used to create a reusable set of instructions.  
  Segments can be created in seperate files or in scripts.  
  If written in a script use `end`, on a seperate line, to mark the end of the list.  
  Segments containing search commands cannot be removed or added.  

  `segment: name_of_segment`
  A segment starts with `segment:` on the first line, followed by the name of the segment.
  This name is what you use to refer to it in scripts.  
  
  You can the write all the scripting commands you want. IE:  
  `segment: example`  
  `@ search uint32 12345`  
  `@ read uint32 repeat 4`  
  `end`  
  This segment will look for 12345 in the file and read 4 uint32's right after each other when run.


# Lists:

  Lists are used to create dropdowns, to limit the users ability to type in incorrect or corrupt values, or to select a known value.
  Lists can be created in seperate files or in scripts.  
  If written in a script use `end`, on a seperate line, to mark the end of the list.

  `list: name_of_list`  
  A list starts with `list:` on the first line, followed by the name of the list.  
  This name is what you use to refer to it in scripts.  
  The name CANNOT contain spaces.
  
  `TYPE: type`  
  TYPE Defines what type the values of the list are. See below for supported types.
  TYPE Is case sensitive, and has to be all-caps.
  
  `Name_for_UI: value`  
  Every entry is structured "name of value: value". The name is shown in the dropdown. The value of the selected name will be written to the file.

  `end`
  If a list is inside a script, use the command `end` to mark the end of the list and continue the rest of the script.

  
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

  signed int 8-64 syntax:
    int8  
    int16  
    int24  
    int32  
    int40  
    int48  
    int56  
    int64  

  float syntax:  
    float32 (single)  
    float64 (double)
  
