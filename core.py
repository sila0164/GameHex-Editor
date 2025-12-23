import struct
import os
import sys
import json
import datetime
#Should never import from anything other than languages

typelengths = {
    'uint8': 1,
    'uint16': 2,
    'uint24': 3,
    'uint32': 4,
    'uint40': 5,
    'uint48': 6,
    'uint56': 7,
    'uint64': 8,
    'int8': 1,
    'int16': 2,
    'int24': 3,
    'int32': 4,
    'int40': 5,
    'int48': 6,
    'int56': 7,
    'int64': 8,
    'float32': 4,
    'float64': 8,
}

validtypes = [
    'uint8', 
    'uint16', 
    'uint24', 
    'uint32', 
    'uint40', 
    'uint48', 
    'uint56', 
    'uint64',
    'int8',
    'int16',
    'int24',
    'int32',
    'int40',
    'int48',
    'int56',
    'int64',
    'float32',
    'float64',
]

class File:
    def __init__(self, path: str):
        import os
        self.path = path
        # reads file as bytes
        with open(path, 'rb+') as f:
            self.hex = f.read()
        self.maxoffset = len(self.hex) # the amount of bytes in file
        self.fullname = os.path.basename(path) # the actual filename (needed to find searchpattern)
        # splits the extension. In case a user wants to run the searchpattern on a file that is "unknown"
        self.name, tempextension = os.path.splitext(self.fullname)
        self.extension = tempextension.lstrip('.') 
        self.stat = {} # a dictionary of all added stats for each file
        self.stat_id = 0
        self.hasbeenwritten = False

    def __repr__(self): #all data contained in the class
        return f'Name: {self.name} \nLength: {self.maxoffset}\n\nStats:\n{self.stat}\n\nFull bytes:\n{self.hex}'

    def readtype(self, typename: str, offset: int, endian):
        typelength = typelengths[typename]
        endoffset = offset + typelength
        valuehex = self.hex[offset:endoffset]
        if 'float32' in typename and endian == 'little':
            valueread = struct.unpack('<f', valuehex)[0]
        elif 'float64' in typename and endian == 'little':
            valueread = struct.unpack('<d', valuehex)[0]
        elif 'float32' in typename and endian == 'big':
            valueread = struct.unpack('>f', valuehex)[0]
        elif 'float64' in typename and endian == 'big':
            valueread = struct.unpack('>d', valuehex)[0]
        elif 'uint' in typename:
            valueread = int.from_bytes(valuehex, byteorder=endian, signed=False) # saves the value as an integer
        elif 'int' in typename:
            valueread = int.from_bytes(valuehex, byteorder=endian, signed=True)
        return valueread

    def saveoffset(self, type: str, title: str, offset: int, endian: str, hide: bool, dict = None): # reads and saves a "stat" from a specific offset
        id = str(self.stat_id)
        self.stat_id += 1
        self.stat[id] = {}
        self.stat[id]['title'] = title
        self.stat[id]["type"] = type # saves the type for writing
        self.stat[id]["offset"] = offset # saves the offset, again for writing
        self.stat[id]["value"] = str(self.readtype(type, offset, endian)) # reads value @ offset
        self.stat[id]['dict'] = dict
        self.stat[id]['endian'] = endian
        self.stat[id]['hidden'] = hide
        if dict != None:
            if not str(self.stat[id]['value']) in self.stat[id]['dict']['list_reverse']: # If the value is not on the list, add it as 'Unknown'
                self.stat[id]['dict']['list'][f'Unknown: ' + type] = str(self.stat[id]['value'])
                self.stat[id]['dict']['list_reverse'][str(self.stat[id]['value'])] = f'Unknown: ' + type
        dev(f'File: New stat: {id} - {title}: {self.stat[id]['value']} - {type} @ {offset}')
            
    def dictsearch(self, dict, type, offset, endian: str, backwards:bool, cap=None) -> int:
        dev(f'File: Searching from dict: For {type} from list. Starting @ {offset}')
        if cap == None:
            cap = self.maxoffset
        else:
            cap = offset + cap
        searchoffset = offset
        search_direction = 1
        if backwards == True:
            search_direction = -1
        while cap > searchoffset:
            search = self.readtype(type, searchoffset, endian)
            if str(search) in dict['list_reverse']:
                dev(f"File: Found {search} @ {offset}")
                return searchoffset
            searchoffset += search_direction
        dev(f"File: Failed to find value in {dict}: Reached {cap}")
        return 0

    def intsearch(self, searchstrings: list, type: str, fromoffset: int, endian: str, backwards:bool, cap=None) -> int:
        dev(f"File: Searching for {searchstrings} as {type} from {fromoffset}")
        searchoffset = fromoffset
        search_direction = 1
        if backwards == True:
            search_direction = -1
        if cap == None:
            cap = self.maxoffset
        else:
            cap = fromoffset + cap
        while cap > searchoffset: 
            search = self.readtype(type, searchoffset, endian)
            if str(search) in searchstrings:
                dev(f"File: Found @ {searchoffset}")
                return searchoffset
            searchoffset += search_direction
        dev(f"File: Failed to find {searchstrings}: Reached {cap}")
        return 0

    def write(self, new_values: list):
        dev('File: Writing to file')
        dev(f'New values: {new_values}')
        with open(self.path, 'rb+') as f: 
            for id in self.stat:
                id_as_int = int(id)
                endian = self.stat[id]['endian']
                new_value = new_values[id_as_int]
                old_value = self.stat[id]['value']
                self.stat[id]['value'] = new_value
                id = self.stat[id]
                if str(old_value) != str(new_value) :
                    dev(f'File: Writing {new_value} as {id['type']} @ {id['offset']} - old: {old_value}')
                    f.seek(id['offset'])
                    typelength = typelengths[id['type']]
                    if 'float32' in id['type'] and endian == 'little':
                        value = float(id['value'])
                        data = struct.pack("<f", value)
                    elif 'float32' in id['type'] and endian == 'big':
                        value = float(id['value'])
                        data = struct.pack(">f", value)
                    elif 'float64' in id['type'] and endian == 'little':
                        value = float(id['value'])
                        data = struct.pack("<d", value)
                    elif 'float64' in id['type'] and endian == 'big':
                        value = float(id['value'])
                        data = struct.pack(">d", value)
                    elif 'uint' in id['type']:
                        data = int(id['value']).to_bytes(typelength, byteorder=endian, signed=False)
                    elif 'int' in id['type']:
                        data = int(id['value']).to_bytes(typelength, byteorder=endian, signed=True)
                    else:
                        error(f'Write: Invalid type: {id['type']}. Please report as a bug.')
                    f.write(data)
                else:
                    dev(f'File: Skipping {id_as_int} - {id['title']}, no new value')
        self.hasbeenwritten = True

def dev(text):
    global settings
    if settings.devdebug == True:
        if text == '':
            print('')
        else:
            print(f'DEV: {text}')

def error(text):
    print(f'\n------------------------------------------------------------------\nERROR:\n{text}\n------------------------------------------------------------------\n', flush=True)
    if settings.is_exe == True:
        date = datetime.datetime.now()
        date_error = (f'ERROR-{date.year}{date.month}{date.day}-{date.hour}{date.minute}{date.second}.txt')
        error_log = os.path.join(settings.root, date_error)
        with open(settings.log, 'r', encoding='utf-8') as logfile:
            error = logfile.read()
        with open(error_log, 'w', encoding="utf-8") as errorlogfile:
            errorlogfile.write(error)
            
def debug(text):
    global settings
    if settings.debug == True:
        if text == '':
            print('')
        else:
            print(f'DEBUG: {text}')

def cleanline(line: str) -> str:
    if '#' in line:
        line_split = line.split('#') # Allaws for comments with # in lines, ignores everything after '#'
        line = line_split[0]
    line = line.strip().replace('&enter&', '\n')
    return line

def readlist(path, language: bool = True) -> tuple[str, dict]:
    """
    Docstring for readlist
    
    :param path: The filepath of the list needed to be loaded
    :return: returns the list as a dictionary
    :rtype: dict[string, string or int]
    """
    returndict = {}
    if language == True:
        returndict['list'] = {}
        returndict['list_reverse'] = {}
    with open(path, encoding='utf-8') as f:
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
            try:
                linewords = line.split(':', maxsplit=2)
                firststring = linewords[0].strip()
                laststring = linewords[1].strip()
                if firststring == 'TYPE':
                    returndict[firststring] = laststring
                elif language == False:
                    returndict[int(firststring)] = laststring
                else:
                    returndict['list'][firststring] = laststring
                    returndict['list_reverse'][laststring] = firststring
            except:
                error(f'List: {name} line {line_number}: incorrect syntax:\n{line}\nIgnoring line...')
            line_number += 1
            line = f.readline()
    return name, returndict

def getlocalizations(localization_folder_path: str) -> tuple[bool, dict]:
    localizations = {}
    for language in os.listdir(localization_folder_path):
        if language.endswith('.ghex'):
            language_path = os.path.join(localization_folder_path, language)
            language_name, language_list = readlist(language_path, False)
            if language_name != '':
                localizations[language_name] = language_list
                print(f'Localization: Loaded language: {language_name}')

    if len(localizations) == 0:
        error('Localization: No languages found!')
        return False, localizations
    return True, localizations

class Settings:
    def __init__(self): # This is only called once at the start, to have default settings.
        self.is_exe = getattr(sys, 'frozen', False)
        if self.is_exe == True:
            self.root = os.path.dirname(sys.executable) # I tilfælde af en exe
        else:
            self.root = os.path.dirname(os.path.abspath(__file__)) # I tilfælde af et script
        os.chdir(self.root)  
        sys.path.append(self.root)
        if self.is_exe == True:
            sys.stdout = open("Log.txt", "w", encoding="utf-8") # Log file creation
            self.log = os.path.join(self.root, "Log.txt") 
        self.suitesfolder = os.path.join(self.root, 'Suites')
        if not os.path.exists(self.suitesfolder):
            os.makedirs(self.suitesfolder, exist_ok=False)
        self.localizationfolder = os.path.join(self.root, 'Localization')
        if not os.path.exists(self.localizationfolder):
            os.makedirs(self.localizationfolder, exist_ok=False)
            error('Settings: No Localizations. Please add at least one localization .ghex file to the "Localization"-folder.')
            sys.exit()
        succes, self.languages = getlocalizations(self.localizationfolder)
        if succes == False:
            error('Settings: No languages found, shutting down. Please make sure there is at least one .ghex localization file in the Localization folder.')
            sys.exit()
        # Default settings in case settings file cant be read
        self.language: str = 'English'
        self.background: str = '#222222'
        self.text: str = '#EEEEEE'
        self.border: str = '#AAAAAA'
        self.highlight: str = '#666666'
        self.accent: str = '#444444'
        self.darkaccent: str = '#333333'
        #self.firstlaunch: bool = True
        #self.wantbackups: bool = False
        self.openfile: bool = False
        self.debug: bool = False
        self.devdebug: bool = False
        print('Settings: Default settings initialized')

    def readsettings(self, force: bool = False) -> bool: # This then reads/creates the settings.json file
        self.settingsfile = os.path.join(self.root, 'Settings.json')
        
        # Loads Settings file if it exists
        if os.path.exists(self.settingsfile) and force == False:
            print('Settings: Importing settings from file')
            with open(self.settingsfile, "r", encoding='utf-8') as f:
                self.settings = json.load(f)
        else:
            force = True
        
        # Creates a new if it doesn't
        if force == True:
            print('Settings: Creating new with defaults')
            self.settings = {
            'text': ["#EEEEEE", "color"],
            'background': ["#222222", 'color'],
            'highlight': ['#666666', 'color'],
            'accent': ['#444444', 'color'],
            'border': ['#AAAAAA', 'color'],
            'darkaccent': ['#333333', 'color'],
            #'firstlaunch': [True, 'bool'],
            'language': ['English', 'language'],
            #'wantbackups': [False, 'bool'], 
            'debug': [False, 'bool'],
            'devdebug': [False, 'bool']
            }
            with open(self.settingsfile, "w", encoding='utf-8') as f:
                json.dump(self.settings, f, indent=1)

        # makes them easily accessible
        self.language = self.languages[self.settings['language'][0]]
        self.background: str = self.settings['background'][0]
        self.text: str = self.settings['text'][0]
        self.border: str = self.settings['border'][0]
        self.highlight: str = self.settings['highlight'][0]
        self.accent: str = self.settings['accent'][0]
        self.darkaccent: str = self.settings['darkaccent'][0]
        #self.firstlaunch: bool = self.settings['firstlaunch'][0]
        #self.wantbackups: bool = self.settings['wantbackups'][0]
        self.openfile: bool = False
        self.debug: bool = self.settings['debug'][0]
        self.devdebug: bool = self.settings['devdebug'][0]

        debug('Debug mode is enabled')
        dev('Devmode is enabled')
        dev(f'Settings: Current Language: {self.language}')

        # Creates backupfolder if there isnt any, if the user wants backups
        #if self.wantbackups == True:
        #    print("Settings: Creating backup folder if there isn't any")
        #    os.makedirs('Backups', exist_ok=True)

        return True

    def getdir(self) -> str:
        return self.root
    
    def change(self, name: str, value) -> bool:
        setting = self.settings[name] # sets the current setting as setting
        success = False
        if isinstance(value, bool) and setting[1] == 'bool': # check if the bool is a bool
            print(f"Settings: Changed: {name} to: {value}")
            success = True
        if isinstance(value, str) and setting[1] == 'color': # checks the string is a valid rgb hex value
            if isinstance(value, str) and value.startswith("#") and len(value) == 7:
                int(value[1:], 16) 
                print(f'Settings: Changed: {name} to: {value}')
                success = True
        if isinstance(value, str) and setting[1] == 'language': # checks if its a supported language
            if value in self.languages:
                print(f'Settings: Changed language to: {value}')
                success = True
        if success == True: # If any checks were succesful it sets the value and saves to settings.json
            setting[0] = value
            with open(self.settingsfile, "w", encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
                return True
        else: # if checks were unsuccessful it return False
            print(f"Settings: Could not change: {name} to: {value} as it was not a: {self.settings[name][1]}")
            return False

settings = Settings()

def forcecreatesettings() -> bool:
    global settings
    print('Settings: Force-creating new settings.json')
    try:
        settings.readsettings(force=True)
        settingsinit = True
    except Exception as e:
        error(f'Settings: Could not force-create settings: {e}')
        settingsinit = False
    return settingsinit

def initsettings() -> bool:
    global settings
    try:
        settings.readsettings()
        settingsinit = True
    except Exception as e:
        error(e)
        settingsinit = False
    return settingsinit                    
        


#------------------------------------------------------------------------------------------
# Everything after this is for translating and using the gh fileformats and scriptlanguage

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

class Suites: # Finished - ADD Ability to have multiple scripts for same filetype.
    def __init__(self):
        if settings == None:
            print('Suites: No Settings')
            return
        self.suites_folder = settings.suitesfolder
        self.supported_extensions = {}
        self.loadedsuites = {}
        self.loadedlists = {}
        debug(f'Suites: Beginning read in {self.suites_folder}')
        for folder in os.listdir(self.suites_folder):
            path = os.path.join(self.suites_folder, folder)
            debug(f'Suites: New suite: {path}')
            self.readsuite(path)
        debug(f'Suites: Read all, supported formats:\n{self.supported_extensions.keys()}\n Lists:\n{self.loadedlists.keys()}')

    def readsuite(self, path):
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
            if 'list' in line_lower:
                name, dictionary = readlist(filepath)
                if name != '':
                    self.loadedlists[name] = dictionary
                    print(f'Suites: List Loaded: {name}')
                    dev(f'{dictionary}')
            elif 'file' in line_lower:
                line_split = line.split(':')
                fileformats = cleanmultientry(line_split[1], separator='/')
                for fileformat in fileformats:
                    self.supported_extensions[fileformat] = filepath
                print(f'Suites: File Format Supported: {fileformat}')
            else:
                error(f'{file} is missing valid definition on line 1:\n {line}')

suites = None

def readsuites() -> bool:
    global suites
    suites = Suites()
    print('Suites: suites have been read')
    return True

class Script: # Unfinished (WIP)
    def __init__(self, file, suites):
        self.dependencies = {}
        self.current_offset = 0
        self.count_unnamed = {}
        self.file = file
        self.suites = suites.supported_extensions
        self.lists = suites.loadedlists
        self.current_endian = 'little'
        self.current_repeat = 0
        self.repeat_multiline = False
        self.first_repeat = True
        self.repeat_type_length = 0
        self.repeat_end = 0
        self.first_search_offset = -1
        self.search_end_repeat = False

    def run(self) -> tuple[bool, str]:
        if self.file.fullname in self.suites:
            script = self.suites[self.file.fullname]
            debug(f'Script: Running script for filename "{self.file.fullname}":')
        else:
            script = self.suites[self.file.extension]
            debug(f'Script: Running script for extension "{self.file.extension}":')
        debug(script + '\n')
        line_number = 2
        with open(script, encoding='utf-8') as f:
            line = f.readline()
            line = f.readline() # Skips the first line as that is only needed for the suite read.
            while line:
                line = cleanline(line)
                debug('')
                debug(f'Line {line_number}: {line}')
                if line == '': # Ignores empty lines
                    debug('Script: skipping empty line')
                    line_number += 1
                    line = f.readline()
                    continue
                try:
                    ui_name, line = getname(line) # This splits the name from the rest of the line and makes the line lower case. Removes comments.
                except:
                    scriptname = os.path.basename(script)
                    error(f'{scriptname} line {line_number}: Invalid Name: {line}')    
                #ADD - Namecheck for duplicates here?
                dev(f'Script: line {line_number}: {line}')
                dev(f'Script: name: {ui_name}')
                line_as_list = line.lower().split(' ') # splits the line into a list for easier reading
                offset = None
                if line[0] == '@': # Check for @ at the beginning of line
                    succes, offset, message = self.readoffset(line_as_list) # Read the offset and move it
                    if succes == False:
                        error(message)
                        return False, message
                    debug(f'{message}')
                    
                    if 'repeat' in line and self.current_repeat == 0:
                        succes, repeat_amount, message = self.repeat(line_as_list)
                        debug(f'Script: {message}')
                        self.current_repeat = repeat_amount
                        self.repeat_start = line_number
                        self.first_repeat = False

                    if 'search' in line:
                        succes1, endian = self.setendian(line_as_list)
                        succes2, message = self.search(offset, line_as_list, line, endian)
                        if succes1 == False or succes2 == False:
                            error(message)
                            return False, message
                        debug(f'{message}')
                        offset = self.current_offset
                        if self.current_repeat != 0:
                            self.current_offset += 1 # If you just repeat a search from the same offset, it will just find the same value again and again.

                    if 'read' in line:
                        if self.search_end_repeat != True:
                            succes1, endian = self.setendian(line_as_list)
                            succes2, message = self.readvalue(offset, line_as_list, endian, ui_name)
                            if succes1 == False or succes2 == False:
                                error(message)
                                return False, message
                            debug(f'{message}')
                        else:
                            self.search_end_repeat = False
                         
                    else: # If no command is given it just moves the offset
                        self.current_offset = offset
                        debug(f'Script: Moved offset to {self.current_offset}')

                elif 'endian' in line_as_list:
                    self.setendian(line_as_list, set_global=True)
                    debug(f'Script: Endian set to {self.current_endian}')

                elif 'repeat' in line_as_list:
                    if 'end' in line_as_list:
                        self.repeat_end = line_number
                        self.current_repeat -= 1
                        dev(f'Script: Repeat end @ line {line_number}')
                    else:
                        succes, repeat_amount, message = self.repeat(line_as_list)
                        debug(f'Script: {message}')
                        self.repeat_start = line_number
                        self.current_repeat = repeat_amount
                        self.repeat_multiline = True
                        dev(f'Script: Repeat start @ line {line_number}')
                
                #elif line.startswith('segment'):
                if self.repeat_multiline == True and self.current_repeat != 0:
                    if line_number == self.repeat_end:
                        line_number = self.repeat_start
                        dev(f'repeating multi line: Remaining: {self.current_repeat}')
                        findline(f, line_number)
                    line = f.readline()
                    line_number += 1

                elif self.repeat_multiline == False and self.current_repeat != 0:
                    self.current_repeat -= 1
                    dev(f'repeating single line: Remaining: {self.current_repeat}')
                    if self.current_repeat == 0:
                        dev(f'Stopping repeat')
                        line = f.readline()
                        self.first_repeat = True
                
                else:
                    line_number += 1
                    self.repeat_multiline = False
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
        if 'repeat' in line:
            self.repeat_type_length = typelengths[read_type]
        hide_value = False
        if 'hidden' in line:
            hide_value = True
        self.file.saveoffset(read_type, ui_name, offset, endian, hide=hide_value, dict=list_from_file)
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

        if self.current_repeat != 0 and self.first_search_offset < 0:
            self.first_search_offset = offset

        #In case cap has been specified
        cap = None
        if 'cap' in line:
            capindex = line_as_list.index('cap')
            capstring = str(line_as_list[capindex + 1])
            success, cap = cleannumber(capstring)
            if success == False:
                return False, f'Invalid cap value: {capstring}'
            
        debug(f'Script: Type to Search: {search_type} - Searchvalue(s): {search_value} - Endian: {endian} - Cap: {cap}\n')

        #much like the readvalue function, but searches for values instead.
        list_from_file = None
        if search_type in validtypes:
            dev(f'Script: Searching for value as type')
            new_offset = self.file.intsearch(search_value, search_type, offset, endian, backwards=backwards, cap=cap)
        elif search_type in self.lists:
            dev(f'Script: Searching for value in list')
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
            self.search_end_repeat = True
            return True, f'Search Reached end of file, resetting to starting offset.'
        else:
            self.current_offset = new_offset

        return True, f'Search {search_type} @ {self.current_offset}'
    
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
        
        




                        


