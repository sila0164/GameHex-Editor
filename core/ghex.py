import os
from core.common import error, debug, dev, validtypes, typelengths
import core.settings as cs
import core.file as cf
import time
import dearpygui.dearpygui as dpg
import gui.mainwindow as mw

def cleanline(line: str) -> str:
    if '#' in line:
        line_split = line.split('#') # Allaws for comments with # in lines, ignores everything after '#'
        line = line_split[0]
    line = line.strip().replace('&enter&', '\n')
    return line

def readlist(path, start: int | None, language: bool = False) -> tuple[str, dict]:
    """
    Docstring for readlist
    
    :param path: The filepath of the list needed to be loaded
    :return: returns the list as a dictionary
    :rtype: dict[string, string or int]
    """
    returndict = {}
    if language == False:
        returndict['list'] = {}
        returndict['list_reverse'] = {}
    with open(path, encoding='utf-8') as f:
        if start != None:
            findline(f, start)
        line = f.readline()
        line = cleanline(line)
        try:
            line_split = line.split(':')
            name = line_split[1].strip()
        except:
            filename = os.path.basename(path)
            error(f'List: {filename}: Could not read name on line 1:\n{line}\nSkipping list...')
            return '', returndict
        line = f.readline()
        line_number = 2
        while line:
            line = cleanline(line)
            if line == '': # Ignores empty lines
                line = f.readline()
                line_number += 1
                continue
            if line.lower().strip() == 'end':
                debug(f'List: Reached end at line {line_number}')
                break
            try:
                linewords = line.split(':', maxsplit=2)
                firststring = linewords[0].strip()
                laststring = linewords[1].strip()
                if firststring == 'TYPE':
                    returndict[firststring] = laststring
                elif language == True:
                    returndict[int(firststring)] = laststring
                else:
                    returndict['list'][firststring] = laststring
                    returndict['list_reverse'][laststring] = firststring
            except:
                error(f'List: {name} line {line_number}: incorrect syntax:\n{line}\nIgnoring line...')
            line_number += 1
            line = f.readline()
    return name, returndict

def findline(f, linenumber: int):
    f.seek(0)
    for lines in range(linenumber):
        f.readline()

def cleannumber(number: str) -> tuple[bool, int]:
    """
    Docstring for cleannumber
    
    :param number: An Integer or Hexvalue as string.
    :type number: str
    :return: Returns Success(bool) and the number as an integer
    :rtype: tuple[bool, int]
    """
    
    if number == '0':
        converted = int(number)
        return True, converted
    
    
    try:
        converted = int(number)
        return True, converted
    except ValueError:
        pass

    try:
        number_no_x = number.removeprefix('0').replace('x', '').replace('X', '')
        converted = int(number_no_x, 16)
        return True, converted
    except ValueError:
        error(f'Invalid number: {number}')
        return False, 0

def getname(line: str) -> tuple[str, str]:
    """
    Docstring for cleanline
    
    :param line: The string to be filtered for '"' or "'". Also removes everything after a '#'.
    :return: returns the name within ' or " and the surrounding text with each word as an entry in a list
    :rtype: tuple[name in "", the words - with name removed - in lower case, with each word as an entry in the list]
    """
    
    if "'" in line:
        split_line = line.split("'", maxsplit=3)
        name = str(split_line[1])
        line = split_line[0] + split_line[2]
    elif '"' in line:
        split_line = line.split('"', maxsplit=3)
        name = str(split_line[1])
        line = split_line[0] + split_line[2]
    else:
        name = ''
        
    return name, line

def cleanmultientry(string: str, separator:str=',') -> list:
    """
    Docstring for cleanmultientry
    
    :param string: Splits up strings at {separator} (if any), removes any '.' prefix and removes ' ' from each entry. Removes any empty strings.
    :param separator: Defaults to ','. Defines what is used to separate each entry in the string
    :return: Returns each entry as a list. If only one is provided it still returns it as a list.
    :rtype: list[str]
    """
    if separator in string:
        stringamount = string.count(separator)
        strings = string.split(separator)
    else:
        stringamount = 0
        strings = [string,]
    while stringamount > -1:
        strings[stringamount] = strings[stringamount].strip().removeprefix('.')
        if strings[stringamount] == '':
            del strings[stringamount] 
        stringamount -= 1 
    return strings

def readarray(path: str, start: int | None) -> tuple[bool, str, dict]:
    returndict = {}
    with open(path, encoding='utf-8') as f:
        if start != None:
            findline(f, start - 1)
        line = f.readline()
        line = cleanline(line)
        try:
            line_split = line.split(':')
            name = line_split[1].strip()
        except:
            filename = os.path.basename(path)
            error(f'Array: {filename}: Could not read name on line 1:\n{line}\nSkipping array...')
            return False, '', returndict
        line = f.readline()
        line_number = 1
        while line:
            line = cleanline(line)
            if line == '': # Ignores empty lines
                line = f.readline()
                line_number += 1
                continue
            if line.lower().strip() == 'end':
                debug(f'Array: Reached end at line {line_number}')
                break
            if 'search' in line:
                error(f'Array: {name} line {line_number}: An array cannot have search commands in them.')
                return False, '', returndict
            if 'function' in line:
                error(f'Array: {name} line {line_number}: An array cannot have function commands in them.')
                return False, '', returndict
            if 'array' in line:
                error(f'Array: {name} line {line_number}: An array cannot have array commands in them.')
                return False, '', returndict
            try:
                returndict[line_number] = line
            except:
                error(f'Array: {name} line {line_number}: incorrect syntax:\n{line}\nIgnoring line...')
            line_number += 1
            line = f.readline()
    return True, name, returndict

def readfunction(path: str, start: int | None) -> tuple[bool, str, dict]:
    returndict = {}
    with open(path, encoding='utf-8') as f:
        if start != None:
            findline(f, start - 1)
        line = f.readline()
        line = cleanline(line)
        try:
            line_split = line.split(':')
            name = line_split[1].strip()
        except:
            filename = os.path.basename(path)
            error(f'Function: {filename}: Could not read name on line 1:\n{line}\nSkipping function...')
            return False, '', returndict
        line = f.readline()
        line_number = 1
        while line:
            line = cleanline(line)
            if line == '': # Ignores empty lines
                line = f.readline()
                line_number += 1
                continue
            if line.lower().strip() == 'end':
                debug(f'Function: Reached end at line {line_number}')
                break
            try:
                returndict[line_number] = line
            except:
                error(f'Function: {name} line {line_number}: incorrect syntax:\n{line}\nIgnoring line...')
            line_number += 1
            line = f.readline()
    return True, name, returndict

class Suites:
    def __init__(self):
        if cs.settings == None:
            print('Suites: No Settings')
            return
        self.suites_folder = cs.settings.suitesfolder
        self.supported_extensions = {}
        self.loaded_suites = {}
        self.loaded_lists = {}
        self.loaded_arrays = {}
        debug(f'Suites: Beginning read in {self.suites_folder}')    
        start = time.time()
    #print(f'Main: Suites Read. 
        for folder in os.listdir(self.suites_folder):
            path = os.path.join(self.suites_folder, folder)
            debug(f'Suites: New suite: {path}')
            self.readsuites(path)
        end = time.time()
        debug(f'Suites: Read all. Time elapsed: {end - start}\nSupported formats:\n{self.supported_extensions.keys()}\nLists:\n{self.loaded_lists.keys()}')

    def readsuites(self, path):
        for file in os.listdir(path):
            debug(f'Suites: reading file: {file}')
            if not file.endswith('.ghex'):
                debug(f'Suites: skipping file {file}, not .ghex')
                continue
            filepath = os.path.join(path, file)
            with open(filepath, encoding='utf-8') as f:
                line = f.readline()
                line = cleanline(line)
                line_lower = line.lower()
            if 'list' in line_lower and ':' in line_lower:
                name, dictionary = readlist(filepath, start=None)
                if name != '':
                    self.loaded_lists[name] = dictionary
                    print(f'Suites: List Loaded: {name}')
                    dev(f'{dictionary}')
            elif 'file' in line_lower:
                line_split = line.split(':')
                fileformats = cleanmultientry(line_split[1], separator='/')
                for fileformat in fileformats:
                    self.supported_extensions[fileformat] = filepath
                    print(f'Suites: File Format Supported: {fileformat}')
            elif 'array' in line_lower and ':' in line_lower:
                success, name, segment = readarray(filepath, start=None)
                if success == False:
                    error(f'Invalid segment: {file}. Skipping...')
                elif name != '':
                    self.loaded_arrays[name] = segment    
                    print(f'Suites: Array Loaded: {name}')
                    dev(f'{segment}')
            else:
                error(f'{file} is missing valid definition on line 1:\n {line}')

suites = Suites()

class Script: # Unfinished (WIP)
    def __init__(self, file, suites):
        self.current_offset = 0 # The current offset that is used throughout a script to read at.
        self.count_unnamed = {} # A dictionary used for dynamically naming unnamed values in a script.
        self.file = file # The currently mounted file to be read
        self.suites = suites.supported_extensions # The list of supported extensions from the Suites-class
        self.lists = suites.loaded_lists # The currently loaded lists from the Suites-class
        self.segments = suites.loaded_arrays # The currently loaded arrays and function from the Suites-class
        self.current_endian = 'little' # Defaults endian. Is used to read values and is changed in the endian related functions.
        self.current_repeat = 0 # A value used to count the number of repeats down when a command is repeated
        self.first_repeat = True # A flag used to allow repeats on combined search and read commands.
        self.repeat_type_length = 0 # This is used if the repeat command is used with read. Moves the offset so that it doesnt just read the same value repeatedly
        self.first_search_offset = -1 # This is used to keep track of the starting offset of a repeated search if it reaches the end of the file.
        self.search_reached_end_of_file = False # A flag used to disable functions when a search reaches end of the file.
        self.function_active = False # This is a flag to change from reading lines in the file to reading line from a function 
        self.function_line = 0 # keeps track of the current function line
        self.array_active = False # This is a flag to change from reading lines in the file to reading line from a array 
        self.array_line = 0 # keeps track of the current array line
        self.repeated_ui_names = {} # used to make multiple values with the same name have a number that itereates after the name.
        self.skip_until_end = False # used to skip lines that are part of a segment or list in a script
        self.functon_buffered_line = None # Used to return to the line when a function is repeated.
        self.array_buffered_line = None # Used to return to the line when an array is repeated.
        self.repeat_active = False # Used to stop reopeats when 0 is reached.
        self.nodes = {} # A dictionary of the nodes to be created in the ui.
        self.current_node = '' #Keeps track of the currently active node (if any)
        self.nested_function_buffer = {} # If a function is run within a function, this will save the state of the current function.
        self.nested_function_counter = 0

    def run(self) -> tuple[bool, str]:
        if self.file.fullname in self.suites:
            script_path = self.suites[self.file.fullname]
            debug(f'Script: Running script for filename "{self.file.fullname}":')
        else:
            script_path = self.suites[self.file.extension]
            debug(f'Script: Running script for extension "{self.file.extension}":')
        debug(script_path + '\n')
        line_number = 2
        with open(script_path, encoding='utf-8') as f:
            line = f.readline()
            line = f.readline() # Skips the first line as that is only needed for the suite read.
            while line:
                self.current_node = '' # Resets the node for each line
                # This is in case we are reading a list or segment. This is done in a seperate function and they return them as a dictionary. We need to skip the lines of the list/segment.
                if self.skip_until_end == True and line.lower().strip() == 'end': #when end is reached continue normal script running.
                    dev('Loop end has been reached')
                    self.skip_until_end = False
                    line = f.readline()
                    line_number += 1
                    continue
                elif self.skip_until_end == True: # when a segment is still being read keep skipping lines
                    dev(f'Skipping line {line_number}')
                    line = f.readline()
                    line_number += 1
                    continue

                # This is when the line gets read (kind of a sorting system)
                buffered_line = line # This is used when a segment is run repeatedly to return to the line that is repeated.
                line = cleanline(line)
                if self.function_active == True:
                    debug('')
                    debug(f'Function line {self.function_line - 1}: {line}')
                elif self.array_active == True:
                    debug('')
                    debug(f'Array line {self.array_line - 1}: {line}')
                else:
                    debug('')
                    debug(f'Line {line_number}: {line}')

                if line == '': # Ignores empty lines
                    debug('Script: skipping empty line')
                    line_number += 1
                    line = f.readline()
                    continue

                # This splits the name from the rest of the line and makes the line lower case. Removes comments.
                ui_name = ''
                try:
                    ui_name, line = getname(line) 
                except:
                    scriptname = os.path.basename(script_path)
                    error(f'{scriptname} line {line_number}: Invalid Name: {line}')    
                
                dev(f'Script: line {line_number}: {line}')
                dev(f'Script: name: {ui_name}')

                # splits the line into a list for easier reading
                line_as_list = line.split(' ') 
                line_as_list_lower = line.lower().split(' ') 
                offset = None

                if self.search_reached_end_of_file == True:
                    line_number += 1
                    line = f.readline()
                    self.search_reached_end_of_file = False
                    self.segment_active = False
                    self.repeat_active = False
                    self.current_repeat = 0
                    continue

                if line[0] == '@': # Check for @ at the beginning of line
                    succes, offset, message = self.readoffset(line_as_list_lower) # Read the offset and move it
                    if succes == False:
                        error(message)
                        return False, message
                    debug(f'{message}')

                    if 'node' in line_as_list_lower:
                        try:
                            self.current_node = line_as_list[line_as_list_lower.index('node') + 1]
                        except:
                            return False, f'"node" command has incorrect/nonexisting name or is missing a name'

                    if 'repeat' in line_as_list_lower and self.repeat_active == False: # if the line contains repeat, set the program to repeat it repeat_amount of times.
                        succes, repeat_amount, message = self.repeat(line_as_list_lower)
                        debug(f'Script: {message}')
                        self.current_repeat = repeat_amount
                        self.repeat_start = line_number
                        self.first_repeat = False
                        self.repeat_active = True

                    if 'search' in line_as_list_lower: # if search is in the line, run the search function and move the offset to the result.
                        succes1, endian = self.setendian(line_as_list_lower)
                        succes2, message = self.search(offset, line_as_list_lower, line, endian)
                        if succes1 == False or succes2 == False:
                            error(message)
                            return False, message
                        debug(f'{message}')
                        offset = self.current_offset

                    if 'read' in line_as_list_lower: # Runs the read function, that reads and sets the value for the ui to use later.
                        succes1, endian = self.setendian(line_as_list_lower)
                        succes2, message = self.readvalue(offset, line_as_list_lower, endian, ui_name)
                        if succes1 == False or succes2 == False:
                            error(message)
                            return False, message
                        debug(f'{message}')

                    if 'array' in line: # run a segment
                        success, message = self.runarray(line_as_list, line_as_list_lower, buffered_line, ui_name)
                        if success == False:
                            error(message)
                            return False, message
                        debug(message)

                    if 'function' in line:
                        success, message = self.runfunction(line_as_list, line_as_list_lower, buffered_line, ui_name)
                        if success == False:
                            error(message)
                            return False, message
                        debug(message)

                    if 'function' not in line and 'array' not in line and 'read' not in line and 'search' not in line: # Changes the offset if no command is given
                        debug(f'No commands detected. Setting offset to: {offset}')
                        self.current_offset = offset
                
                # '@' commands are done here and the following commands are seperate.

                # Creates and saves a segment to be run later
                elif 'array:' in line_as_list_lower: 
                    self.skip_until_end = True
                    success, name, segment = readarray(script_path, start=line_number)
                    if success == False:
                        return False, 'Script: Invalid Array'
                    if name != '':
                        self.segments[name] = segment    
                        print(f'Script: Array Loaded: {name}')
                        debug(f'Array name: {name}') 
                        debug(f'{segment}')

                elif 'function:' in line_as_list_lower: 
                    self.skip_until_end = True
                    success, name, segment = readarray(script_path, start=line_number)
                    if success == False:
                        return False, 'Script: Invalid Function'
                    if name != '':
                        self.segments[name] = segment    
                        print(f'Script: Function Loaded: {name}')
                        debug(f'Array name: {name}') 
                        debug(f'{segment}')

                # Creates and saves a list to be used later
                elif 'list:' in line_as_list_lower:
                    self.skip_until_end = True
                    name, dictionary = readlist(script_path, start=line_number)
                    if name != '':
                        self.lists[name] = dictionary
                        print(f'Script: List Loaded: {name}')
                        dev(f'{dictionary}')

                # Creates and saves a note that values and segments can be added to.
                elif 'node:' in line_as_list_lower and 'end' not in line_as_list_lower:
                    node_name = line_as_list[line_as_list_lower.index('node:') + 1]
                    if ui_name == '':
                        if 'Node' not in self.count_unnamed:
                            self.count_unnamed['Node'] = 0
                        self.count_unnamed['Node'] += 1
                        number = str(self.count_unnamed['Node'])
                        ui_name = 'Node' + ' ' + number
                    if ui_name not in self.repeated_ui_names:
                        self.repeated_ui_names[ui_name] = 0
                    self.repeated_ui_names[ui_name] += 1
                    if self.repeated_ui_names[ui_name] != 1:
                        ui_name = ui_name + ' ' + str(self.repeated_ui_names[ui_name])
                    parent = None
                    if 'node' in line_as_list_lower:
                        try:
                            self.current_node = line_as_list[line_as_list_lower.index('node') + 1]
                            parent = self.current_node
                        except:
                            return False, f'"node" command is missing a name after it'

                    self.file.saveparent(ui_name, removable=False, parent=parent)
                    self.nodes[node_name] = ui_name
                    self.current_node = node_name

                # Sets the global endian if endian is in the line and alone. 
                elif 'endian' in line_as_list_lower:
                    self.setendian(line_as_list_lower, set_global=True)
                    debug(f'Script: Endian set to {self.current_endian}')
                
                #No more commands. This is logic for repeat loops.
                if self.current_repeat != 0 and self.function_active == False:
                    self.current_repeat -= 1
                    if 'search' in line_as_list and 'read' not in line_as_list:
                        self.current_offset = self.current_offset + 1
                    dev(f'repeating single line: Remaining: {self.current_repeat}')

                    if self.current_repeat == 0:
                        dev(f'Stopping repeat')
                        line = f.readline()
                        self.first_repeat = True
                    continue
                
                #This is the default behaviour. If a segment is active it reads from the segment dictionary, not the file.
                if self.function_active == True and self.function_line not in self.function:
                    dev('Setting self.function_active to False')
                    self.function_active = False
                    if self.nested_function_buffer != {}:
                        dev('Going back to nested function')
                        self.recallfunction()
                    line = self.function_buffered_line
                    dev(line)
                elif self.function_active == True:
                    line = self.function[self.function_line]
                    self.function_line += 1
                elif self.array_active == True and self.array_line not in self.array:
                    dev('Setting self.array_active to False')
                    self.array_active = False
                    line = self.array_buffered_line
                    dev(line)
                elif self.array_active == True:
                    line = self.array[self.array_line]
                    self.array_line += 1
                else:
                    line_number += 1
                    self.repeat_active = False
                    self.array_active = False
                    line = f.readline()
        print('Script: Finished')
        return True, 'Script ran successfully'

    def readoffset(self, line: list) -> tuple[bool, int, str]:

        if line[0] == '@':
            offset = line[1].lower()
        else:
            return False, -1, 'Syntax error at "@", check that there is a space after "@"'
        dev(f'offset is {offset}')

        if 'repeat' in line and self.first_repeat == False and 'search' not in line: # If a read is repeated it adds the typelength to the offset
            offset = self.current_offset + self.repeat_type_length
            self.current_offset = offset
            return True, offset, f'Repeat offset set to {offset}'

        if 'read' in offset or 'search' in offset: #If the offset is read it uses the general offset
            offset = self.current_offset
            dev(f'offset set to current {offset}')
            del line[0]
        elif '+' in offset: #If the offset string contains '+' or '-' add it to self.currentoffset
            offset = offset.removeprefix('+')
            success, offset = cleannumber(offset)
            dev('adding to offset')
            if success == True:
                self.current_offset = self.current_offset + offset
                offset = self.current_offset
                dev(str(offset))
            else: 
                return False, -1, 'Invalid value for offset'
            del line[0:2]
        elif '-' in offset:
            offset = offset.removeprefix('-')
            success, offset = cleannumber(offset)
            dev('subtracting from offset')
            if success == True:
                self.current_offset = self.current_offset - offset
                offset = self.current_offset
                dev(str(offset))
            else: 
                return False, -1, 'Invalid value for offset'
            del line[0:2]
        else:
            dev(f'setting to {offset}')
            success, offset = cleannumber(offset)
            if success == False:
                return False, -1, 'Offset value is invalid'
            self.current_offset = offset
            dev('set')
            del line[0:2]

        return True, offset, f'Offset set to {offset}'

    def readvalue(self, offset: int, line: list, endian: str, ui_name: str) -> tuple[bool, str]: 
        readindex = line.index('read')
        read_type = line[readindex + 1]
        dev(f'Script: Type/list to read: {read_type} - Endian: {endian}')
        list_from_file = None
        
        if read_type in validtypes:
            debug(f'Script: reading as type: "{read_type}" - Endian: {endian}')
        elif read_type in self.lists:
            list_from_file = self.lists[read_type]
            debug(f'Script: running from list "{read_type}" - Endian: {endian}')
            try:
                read_type = list_from_file['TYPE']
            except:
                return False, f'{read_type} is missing TYPE definition'
        else:
            return False, f'"{read_type}" is not a valid type or list'
        
        if offset + typelengths[read_type] > self.file.maxoffset: # Stops the program from reading beyond the end of the file.
            self.current_repeat = 0 # Stops any repeats if they are running
            return True, f'Reached end of file'
        
        if ui_name == '':
            if read_type not in self.count_unnamed:
                self.count_unnamed[read_type] = 0
            self.count_unnamed[read_type] += 1
            number = str(self.count_unnamed[read_type])
            ui_name = read_type + ' ' + number
        if ui_name not in self.repeated_ui_names:
            self.repeated_ui_names[ui_name] = 0
        self.repeated_ui_names[ui_name] += 1
        if self.repeated_ui_names[ui_name] != 1:
            ui_name = ui_name + ' ' + str(self.repeated_ui_names[ui_name])

        hide_value = False
        if 'hidden' in line:
            hide_value = True
        
        new_value = None
        if 'value' in line: # Allows to change a value from the script.
            value_index = line.index('value') + 1
            try:
                new_value = line[value_index]
            except:
                return False, f'Value command has no value after it'
            if 'float' in read_type:
                try:
                    new_value = float(new_value)
                except ValueError:
                    return False, f'{new_value} is not a valid float'
            elif 'int' in read_type:
                try:
                    new_value = int(new_value)
                except ValueError:
                    return False, f'{new_value} is not a valid integer'
            debug(f'Presetting to {new_value}')

        if self.array_active == True:
            parent = self.array_name
        elif self.current_node != '':
            parent = self.nodes[self.current_node]
        else:
            parent = self.current_node


        removable = False
        if 'removable' in line:
            removable = True

        self.current_offset = offset + typelengths[read_type]

        self.file.saveoffset(read_type, ui_name, offset, endian, hide=hide_value, removable = removable, newvalue=new_value, dict=list_from_file, parent=parent)
        return True, f'Read {read_type} @ {offset} as {ui_name}'

    def search(self, offset: int, line_as_list: list, line: str, endian: str) -> tuple[bool, str]:
        
        backwards = False
        if '-search' in line_as_list:
            searchindex = line_as_list.index('-search')
            backwards = True
        elif 'search' in line_as_list:
            searchindex = line_as_list.index('search')
        search_type = line_as_list[searchindex + 1]
        search_value = cleanmultientry(line)
        # To support searching for multiple values, and allow free placement of search on a line, the below removes any text before and after the values.
        search_value[0] = line_as_list[searchindex + 2].replace(',', '')
        search_value[-1] = search_value[-1].split(' ')[0]

        if self.current_repeat != 0 and self.first_search_offset < 0: # Sets first_search_offset if needed to revert (end of file)
            self.first_search_offset = offset
            dev(f'Set return offset {self.first_search_offset}')

        #In case cap has been specified
        cap = None
        if 'cap' in line:
            capindex = line_as_list.index('cap')
            capstring = str(line_as_list[capindex + 1])
            success, cap = cleannumber(capstring)
            if success == False:
                return False, f'Invalid cap value: {capstring}'
            if backwards == True and cap > 0:
                cap = cap * -1
            if backwards == False and cap < 0:
                cap = cap * -1
            if cap == 0:
                cap = None

        #much like the readvalue function, but searches for values instead.
        list_from_file = None
        if search_type in validtypes:
            debug(f'Script: Type to Search: {search_type} - Searchvalue(s): {search_value} - Endian: {endian} - Cap: {cap}')
            new_offset = self.file.intsearch(search_value, search_type, offset, endian, backwards=backwards, cap=cap)
        elif search_type in self.lists:
            debug(f'Script: List to Search: {search_type} - Endian: {endian} - Cap: {cap}')
            list_from_file = self.lists[search_type]
            try:
                search_type = list_from_file['TYPE']
                new_offset = self.file.dictsearch(list_from_file, search_type, offset, endian, backwards=backwards, cap=cap)
            except:
                return False, f'"{search_type}" is missing "TYPE" definition'
        else:
            return False, f'"{search_type}" is not a valid type or list'
        
        # The searchfunctions return 0 if they couldnt find the value.
        if new_offset == 0 and self.current_repeat == 0:
            return False, f'Could not find {search_value} in file'
        elif new_offset == 0 and self.current_repeat != 0:
            self.current_repeat = 0
            self.current_offset = self.first_search_offset
            self.first_search_offset = -1
            self.search_reached_end_of_file = True
            self.repeat_active = False
            self.segment_active = False
            return True, f'Search Reached end of file, resetting to starting offset.'
        else:
            self.current_offset = new_offset

        return True, f'Found {search_type} @ {self.current_offset}'
    
    def repeat(self, line_as_list: list) -> tuple[bool, int, str]:
        repeat_index = line_as_list.index('repeat')
        repeat_amount = line_as_list[repeat_index + 1]
        succes, repeat_amount = cleannumber(repeat_amount)
        if succes == False:
            return False, 0, f'Invalid repeat value: {repeat_amount}'
        if repeat_amount < -1:
            return False, 0, f'Invalid repeat value: {repeat_amount}, repeat does not support negative values'
        
        return True, repeat_amount, f'Repeating {repeat_amount} times'

    def setendian(self, line_as_list: list, set_global: bool = False) -> tuple[bool, str]:
        if 'endian' not in line_as_list:
            current_endian = self.current_endian
            return True, current_endian
        if 'big' in line_as_list:
            current_endian = 'big'
            if set_global == True:
                self.current_endian = current_endian 
            return True, current_endian
        elif 'little' in line_as_list:
            current_endian = 'little'
            if set_global == True:
                self.current_endian = current_endian 
            return True, current_endian
        else:
            return False, 'Script: Incorrect syntax for endian command'
        
    def runarray(self, line_as_list: list, line_as_list_lower: list, buffered_line: str, ui_name: str) -> tuple[bool, str]:
        try:
            array_name = line_as_list[line_as_list_lower.index('array') + 1]
        except:
            return False, f'Array is missing function name after command.'
        self.array_buffered_line = buffered_line

        removable = False
        if 'removable' in line_as_list_lower:
            removable = True
        
        if ui_name == '':
            if 'Array' not in self.count_unnamed:
                self.count_unnamed['Array'] = 0
            self.count_unnamed['Array'] += 1
            number = str(self.count_unnamed['Array'])
            ui_name = 'Array' + ' ' + number
        if ui_name not in self.repeated_ui_names:
            self.repeated_ui_names[ui_name] = 0
        self.repeated_ui_names[ui_name] += 1
        if self.repeated_ui_names[ui_name] != 1:
            ui_name = ui_name + ' ' + str(self.repeated_ui_names[ui_name])

        if array_name in self.segments:
            self.array = self.segments[array_name]
            self.array_name = ui_name
            self.array_active = True
            self.array_line = 1
            parent = None
            if self.current_node != '':
                parent = self.nodes[self.current_node]
            self.file.saveparent(self.array_name, removable=removable, parent = parent)
        else:
            return False, f'Array {array_name} not found'

        return True, f'Array started succesfully'     
    
    def runfunction(self, line_as_list: list, line_as_list_lower: list, buffered_line: str, ui_name: str) -> tuple[bool, str]:
        if self.function_active == True:
            self.nested_function_buffer[self.nested_function_counter] = {}
            self.nested_function_buffer[self.nested_function_counter]['name'] = self.function_name
            self.nested_function_buffer[self.nested_function_counter]['current line'] = self.function_line
            self.nested_function_counter += 1
        try:
            function_name = line_as_list[line_as_list_lower.index('function') + 1]
        except:
            return False, f'Function is missing function name after command.'
        self.function_buffered_line = buffered_line

        if function_name in self.segments:
            self.function = self.segments[function_name]
            self.function_name = ui_name
            self.function_active = True
            self.function_line = 1
        else:
            return False, f'Function {function_name} not found'

        return True, f'Function started succesfully'   
    
    def recallfunction(self):
        self.nested_function_counter -= 1
        self.function_name = self.nested_function_buffer[self.nested_function_counter]['name']
        self.function_line = self.nested_function_buffer[self.nested_function_counter]['current line']
        self.function = self.segments[self.function_name]
        del self.nested_function_buffer[self.nested_function_counter]

def run_script():
    script = Script(cf.current_file, suites)
    dpg.configure_item(item='message_display', label=cs.settings.language[17])
    success = script.run()
    if success == False:
        dpg.configure_item(item='message_display', label=cs.settings.language[32])
    else:
        dpg.configure_item(item='message_display', label=cs.settings.language[31])
    if mw.editor_is_built == False:
        mw.build_editor()
    dev(script.file)
    mw.add_file_tab(cf.current_file)