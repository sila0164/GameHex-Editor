import struct
from localization import languages
import os
import sys
import json
#Should never import from anything other than languages

typelengths = {
    'int8': 1,
    'int16': 2,
    'int24': 3,
    'int32': 4,
    'int40': 5,
    'int48': 6,
    'int56': 7,
    'int64': 8,
    'float': 4,
    'doublefloat': 8,
}

validtypes = [
    'int8', 
    'int16', 
    'int24', 
    'int32', 
    'int40', 
    'int48', 
    'int56', 
    'int64', 
    'float',
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
        self.hasbeenwritten = False

    def __repr__(self): #all data contained in the class
        return f'Name: {self.name} \nLength: {self.maxoffset}\n\nStats:\n{self.stat}\n\nFull bytes:\n{self.hex}'

    def readtype(self, typename: str, offset: int):
        typelength = typelengths[typename]
        endoffset = offset + typelength
        valuehex = self.hex[offset:endoffset]
        if 'float' in typename:
            valueread = struct.unpack('<f', valuehex)[0] #saves value as float
        if 'int' in typename:
            valueread = int.from_bytes(valuehex, byteorder='little') # saves the value as an integer
        return valueread

    def saveoffset(self, typename: str, name: str, offset: int, dict = None): # reads and saves a "stat" from a specific offset
        self.stat[name] = {} # the name of the stat (I think this might be rudundant)
        self.stat[name]["typename"] = typename # saves the type for writing
        self.stat[name]["offset"] = offset # saves the offset, again for writing
        self.stat[name]["value"] = self.readtype(typename, offset) # reads value @ offset
        self.stat[name]['write'] = 0 # set the write stat. this is changed to 1 if the value changes
        self.stat[name]['dict'] = dict
        if dict != None:
            self.stat[name]['dict'] = dict.copy()
            del self.stat[name]['dict']['TYPE']
            self.stat[name]['dict_reverse'] = {v: k for k, v in self.stat[name]['dict'].items()}
            if not str(self.stat[name]['value']) in self.stat[name]['dict_reverse']: # If the value is not on the list, add it as 'Unknown'
                self.stat[name]['dict']['Unknown'] = str(self.stat[name]['value'])
                self.stat[name]['dict_reverse'] = {v: k for k, v in self.stat[name]['dict'].items()}
        debug(f'File: New stat: {name}, {self.stat[name]['value']}, {typename}, @ {offset}')
            
    def dictsearch(self, dict, typename, offset, backwards:bool, cap=None) -> int:
        debug(f'File: Searching from dict: For {typename}. From {dict}. Starting @ {offset}')
        if cap == None:
            cap = self.maxoffset
        else:
            cap = offset + cap
        tempdict = dict.copy()
        del tempdict['TYPE']
        dict_reverse = {v: k for k, v in dict.items()}
        searchoffset = offset
        search_direction = 1
        if backwards == True:
            search_direction = -1
        while cap > searchoffset:
            search = self.readtype(typename, searchoffset)
            if str(search) in dict_reverse:
                debug(f"File: Found {search} @ {offset}")
                del tempdict
                return searchoffset
            searchoffset += search_direction
        debug(f"File: Failed to find {dict}: Reached {cap}")
        del tempdict
        return 0

    def intsearch(self, searchstrings: list, typename: str, fromoffset: int, backwards:bool, cap=None) -> int:
        debug(f"File: Searching for {searchstrings} as {typename} from {fromoffset}")
        searchoffset = fromoffset
        search_direction = 1
        if backwards == True:
            search_direction = -1
        if cap == None:
            cap = self.maxoffset
        else:
            cap = fromoffset + cap
        while cap > searchoffset: 
            search = self.readtype(typename, searchoffset)
            if str(search) in searchstrings:
                debug(f"File: Found @ {searchoffset}")
                return searchoffset
            searchoffset += search_direction
        debug(f"File: Failed to find {searchstrings}: Reached {cap}")
        return 0

    def changevalue(self, name:str, value): # changes current value for a stat which will be written if wanted
        self.stat[name]['value'] = value # updates the value !!This is not in the file, this is a buffer in memory!!
        self.stat[name]['write'] = 1 # A flag that tells the writefunction, that it should write this on the next write.
        debug(f'File: New value set: {name} - {value}')

    def write(self):
        debug('File: Writing to file')
        with open(self.path, 'rb+') as f: # opens the file
            for index, statname in enumerate(self.stat): # goes through all stats
                stat = self.stat[statname]
                if stat['write'] == 1: # Checks Write flag
                    debug(f'File: Writing {stat['value']} @ {stat['offset']} as {stat['typename']}')
                    f.seek(stat['offset']) # finds the stats offset
                    typelength = typelengths[stat['typename']]
                    if stat['typename'] == 'float': # if float use struct
                        value = float(stat['value'])
                        data = struct.pack("<f", value)
                    else: # else use int_tobytes.
                        data = int(stat['value']).to_bytes(typelength, byteorder="little")
                    f.write(data) # writes the value to a given offset
                    stat['write'] = 0 # sets the write to 0 until it is changed again
                else:
                    debug(f'File: Skipping {stat}, no new value') # skips if write is not 1
        self.hasbeenwritten = True



class Settings:
    def __init__(self, force: bool = False):
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

        self.settingsfile = os.path.join(self.root, 'Settings.json')
        self.suitesfolder = os.path.join(self.root, 'Suites')

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
            'firstlaunch': [True, 'bool'],
            'language': ['english', 'language'],
            'wantbackups': [False, 'bool'], 
            'debug': [False, 'bool'],
            }
            with open(self.settingsfile, "w", encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)

        # makes them easily accessible
        self.language = languages[self.settings['language'][0]]
        self.background: str = self.settings['background'][0]
        self.text: str = self.settings['text'][0]
        self.border: str = self.settings['border'][0]
        self.highlight: str = self.settings['highlight'][0]
        self.accent: str = self.settings['accent'][0]
        self.darkaccent: str = self.settings['darkaccent'][0]
        self.firstlaunch: bool = self.settings['firstlaunch'][0]
        self.wantbackups: bool = self.settings['wantbackups'][0]
        self.openfile: bool = False
        self.debug: bool = self.settings['debug'][0]

        # gets suites from files
        #self.getsuites()

        # Creates backupfolder if there isnt any, if the user wants backups
        if self.wantbackups == True:
            print("Settings: Creating backup folder if there isn't any")
            os.makedirs('Backups', exist_ok=True)

    def getdir(self) -> str:
        return self.root
    
    def getlog(self, add=None) -> str:
        print(flush=True)
        if add != None:
            print(add)
        logtext = 'Test'
        if self.is_exe == True:
            with open(self.log, "r", encoding="utf-8") as f:
                logtext = f.read()
        return logtext
    
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
            if value in languages:
                print(f'Settings: Changed language to: {value}')
                success = True
        if success == True: # If any checks were succesful it sets the value and saves to settings.json
            setting[0] = value
            with open(self.settingsfile, "w") as f:
                json.dump(self.settings, f, indent=4)
                return True
        else: # if checks were unsuccessful it return False
            print(f"Settings: Could not change: {name} to: {value} as it was not a: {self.settings[name][1]}")
            return False

settings = None

def debug(text):
    global settings
    if settings != None and settings.debug == True:
        print(f'DEBUG: {text}')

def forcecreatesettings() -> bool:
    global settings
    print('Settings: Force-creating new settings.json')
    try:
        settings = Settings(force=True)
        settingsinit = True
    except Exception as e:
        print('Settings: Could not force-create settings:', e)
        settingsinit = False
    return settingsinit

def initsettings() -> bool:
    global settings
    print('Settings: Initializing settings')
    try:
        settings = Settings()
        settingsinit = True
        print('Settings: Settings Initialized')
    except Exception as e:
        print('Settings: Could not initialize settings:', e)
        settingsinit = False
    return settingsinit                    
        


#------------------------------------------------------------------------------------------
# Everything after this is for translating and using the gh fileformats and scriptlanguage



def cleanline(line: str) -> str:
    if '#' in line:
        line_split = line.split('#') # Allaws for comments with # in lines, ignores everything after '#'
        line = line_split[0]
    line = line.strip()
    return line

def getname(line: str) -> tuple[str, str]:
    """
    Docstring for cleanline
    
    :param line: The string to be filtered for '"' or "'". Also removes everything after a '#'.
    :return: returns the name within ' or " and the surrounding text with each word as an entry in a list
    :rtype: tuple[name in "", the words - with name removed - in lower case, with each word as an entry in the list]
    """
    
    if '"' in line:
        split_line = line.split('"', maxsplit=3)
        name = str(split_line[1])
        line = split_line[0] + split_line[2]
    elif "'" in line:
        split_line = line.split("'", maxsplit=3)
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

def readlist(path) -> tuple[str, dict]:
    """
    Docstring for readlist
    
    :param path: The filepath of the list needed to be loaded
    :return: returns the list as a dictionary
    :rtype: dict[string, string or int]
    """
    returndict = {}
    with open(path) as f:
        line = f.readline()
        line = cleanline(line)
        line_split = line.split(':')
        name = line_split[1].strip()
        line = f.readline()
        while line:
            line = cleanline(line)
            if line == '': # Ignores empty lines
                debug('Read List: skipping empty line')
                line = f.readline()
                continue
            linewords = line.split(':', maxsplit=2)
            firststring = linewords[0].strip()
            laststring = linewords[1].strip()
            debug(f'Read List: {firststring} - {laststring}')
            returndict[firststring] = laststring
            line = f.readline()
        debug(f'Read List: {name}:\n{returndict}')
    return name, returndict


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
        print(f'Suites: Read all, supported formats:\n{self.supported_extensions}\n Lists:\n{self.loadedlists}')

    def readsuite(self, path):
        for file in os.listdir(path):
            debug(f'Suites: reading file: {file}')
            if not file.endswith('.ghex'):
                debug(f'Suites: skipping file {file}, not .ghex')
                continue
            filepath = os.path.join(path, file)
            with open(filepath) as f:
                line = f.readline()
                line = cleanline(line)
                line_lower = line.lower()
            if 'list' in line_lower:
                name, dictionary = readlist(filepath)
                self.loadedlists[name] = dictionary
                debug(f'Suites: List Read: {name} - {dictionary}')
            elif 'file' in line_lower:
                line_split = line.split(':')
                fileformats = cleanmultientry(line_split[1], separator=',')
                for fileformat in fileformats:
                    self.supported_extensions[fileformat] = filepath
                debug(f'Suites: File Format Supported: {fileformat} - {filepath}')
            else:
                print(f'Suites: {file} missing definition on line 1')

suites = None

def readsuites() -> bool:
    global suites
    #try:
    suites = Suites()
    print('Suites: suites have been read')
    return True
    #except Exception as e:
    #    print(f'Suites: Could not read suites:\n{e}')
    #    return False

class Script: # Unfinished (WIP)
    def __init__(self, file, suites):
        self.dependencies = {}
        self.current_offset = 0
        self.count_unnamed = {}
        self.file = file
        self.suites = suites.supported_extensions
        self.lists = suites.loadedlists

    def run(self) -> tuple[bool, str]:
        if self.file.fullname in self.suites:
            script = self.suites[self.file.fullname]
            debug(f'Script: Running from filename: {self.file.fullname}')
        else:
            script = self.suites[self.file.extension]
            debug(f'Script: Running from extension: {self.file.extension}')
        debug(script)
        line_number = 1
        with open(script) as f:
            line = f.readline()
            debug(line)
            line = f.readline() # Skips the first line as that is only needed for the suite read.
            while line:
                debug(line)
                line = cleanline(line)
                if line == '':# Ignores empty lines
                    debug('Script: skipping empty line')
                    line_number += 1
                    line = f.readline()
                    continue
                ui_name, line = getname(line) # This splits the name from the rest of the line and makes the line lower case. Removes comments.
                #ADD - Namecheck for duplicates here?
                debug(f'Script: line {line_number}: {line}')
                debug(f'Script: name: {ui_name}')
                line_as_list = line.lower().split(' ') # splits the line into a list for easier reading
                offset = None
                if line[0] == '@': # Check for @ at the beginning of line
                    succes, offset, message = self.readoffset(line_as_list) # Read the offset and move it
                    if succes == False:
                        return False, message
                    debug(message)
                    if 'read' in line and 'search' not in line: # If it is read only
                        succes, message = self.readvalue(offset, line_as_list, ui_name)
                        if succes == False:
                            return False, message
                        debug(message)
                    elif 'search' in line and 'read' not in line: # If it is search only
                        succes, message = self.search(offset, line_as_list, line)
                        if succes == False:
                            return False, message
                        debug(message)
                    elif 'search' in line and 'read' in line: # If it is both search and read
                        succes, message = self.search(offset, line_as_list, line)
                        if succes == False:
                            return False, message
                        debug(message)
                        succes, message = self.readvalue(self.current_offset, line_as_list, ui_name)
                        if succes == False:
                            return False, message
                        debug(message)
                    else: # If no command is given it just moves the offset
                        self.current_offset = offset
                        debug(f'Script: Moved offset to {self.current_offset}')
                #elif line.startswith('segment'):
                    
                line_number += 1
                line = f.readline()
        return True, 'Script ran successfully'

    def readoffset(self, line: list) -> tuple[bool, int, str]: #ADD ability to read hex value and not just integers

        if line[0] == '@':
            offset = line[1].lower()
        else:
            return False, -1, 'Syntax error at "@", check that there is a space after "@"'
     
        # ADD Check for hex value and that it can be converted to integer.
        if 'read' in offset or 'search' in offset: #If the offset is read it uses the general offset
            offset = self.current_offset
            del line[0]
        elif '+' in offset or '-' in offset: #If the offset string contains '+' or '-' add it to self.currentoffset
            self.current_offset = self.current_offset + int(offset)
            offset = self.current_offset
            del line[0:2]
        else:
            try:
                offset = int(offset) 
                self.current_offset = offset
                del line[0:2]
            except:
                return False, -1, 'Offset value is not an integer. check that there is a space after "@" and that the value is a valid integer.'

        return True, offset, f'Offset set to {offset}'

    def readvalue(self, offset: int, line: list, ui_name: str) -> tuple[bool, str]: # Unfinished
        readindex = line.index('read')
        read_type = line[readindex + 1]
        debug(f'Script: Type to Read: {read_type}')
        list_from_file = None
        if read_type in validtypes:
            debug(f'Script: readvalue: type to read: {read_type}')
        elif read_type in self.lists:
            list_from_file = self.lists[read_type]
            try:
                read_type = list_from_file['TYPE']
            except:
                print(f'Script: readvalue: List {read_type} is missing TYPE definition\n{list_from_file}')
                return False, 'List is missing TYPE definition'
        else:
            print(f'Script: readvalue: "{read_type}" is not a valid type or list')
            return False, f'"{read_type}" is not a valid type or list'
        if ui_name == '':
            if read_type not in self.count_unnamed:
                self.count_unnamed[read_type] = 0
            self.count_unnamed[read_type] += 1
            number = str(self.count_unnamed[read_type])
            ui_name = read_type + ' ' + number
        self.file.saveoffset(read_type, ui_name, offset, dict=list_from_file)
        return True, f'Read {read_type} @ {offset} as {ui_name}'

    def search(self, offset: int, line_as_list: list, line: str) -> tuple[bool, str]:
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
        #In case cap has been specified
        cap = None
        if 'cap' in line:
            capindex = line_as_list.index('cap')
            try:
                cap = int(line_as_list[capindex + 1])
            except:
                if capindex + 1 in line_as_list:
                    return False, f'Invalid cap value: {line_as_list[capindex+1]}'
                return False, 'No cap value given.'
        debug(f'Script: Type to Search: {search_type}\nSearchvalue(s): {search_value}')
        #much like the readvalue function, but searches for values instead.
        list_from_file = None
        if search_type in validtypes:
            debug(f'Script: Search: type to search: {search_type}')
            new_offset = self.file.intsearch(search_value, search_type, offset, backwards=backwards, cap=cap)
        elif search_type in self.lists:
            list_from_file = self.lists[search_type]
            try:
                search_type = list_from_file['TYPE']
                new_offset = self.file.dictsearch(list_from_file, search_type, offset, backwards=backwards, cap=cap)
            except:
                print(f'Script: search: List "{search_type}" is missing TYPE definition\n{list_from_file}')
                return False, f'"{search_type}" is missing TYPE definition'
        else:
            print(f'Script: search: "{search_type}" is not a valid type or list')
            return False, f'"{search_type}" is not a valid type or list'
        # The searchfunctions return 0 if they couldnt find the value.
        if new_offset == 0:
            print(f'Script: search: Could not find {search_value}')
            return False, f'Could not find {search_value} in file'
        else:
            self.current_offset = new_offset

        return True, f'Search {search_type} @ {self.current_offset}'

        




                        


