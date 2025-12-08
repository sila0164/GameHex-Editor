import struct
from db.weapondb import weapondb
from localization import languages
import os
import sys
import json


#Should never import from anything other than languages

file = None # This is where the currently opened file is saved and accessed

class File:
    def __init__(self, path: str):
        import os
        self.path = path
        # reads file as bytes
        with open(path, 'rb+') as f:
            self.hex = f.read()
        # begins indexing the different parameters
        idhex = self.hex[1:9]
        self.id = int.from_bytes(idhex, byteorder='little') # the id is a unique int64 in every file
        self.maxoffset = len(self.hex) # the amount of bytes in file
        self.fullname = os.path.basename(path) # the actual filename (needed to find searchpattern)
        # splits the extension. In case a user wants to run the searchpattern on a file that is "unknown"
        self.name, tempextension = os.path.splitext(self.fullname)
        self.extension = tempextension.lstrip('.') 
        self.stat = {} # a dictionary of all added stats for each file
        self.hasbeenwritten = False

    def __repr__(self): #all data contained in the class
        return f'Name: {self.name} \nId: {self.id}\nLength: {self.maxoffset}\n\nStats:\n{self.stat}\n\nFull bytes:\n{self.hex}'
    
    def hassupport(self):
        #if self.extension in settings.supportedfiles: # Checks if file is supported
        if self.extension == 'GR_WeaponDBEntry':
            for index, name in enumerate(weapondb): # checks for confirmed support
                id = weapondb[name]
                if self.id == id:
                    debug(f'File: Confirmed ID Found: {name} - {id}')
                    return 'confirmed'
            debug('File: Supported fileformat found')
            return 'unknown' # returns that it is a known fileformat, but it isnt confirmed to be working
        debug('File: Unsupported file')
        return 'unsupported' # returns the file is unsupported
    
    def mount(self):
        global current
        current = self
        debug(f'File: {self.name} mounted')

    def readtype(self, typename: str, offset: int):
        if typename == 'float':
            valuehex = self.hex[offset:offset+4]
            valueread = struct.unpack('<f', valuehex)[0] #saves value as float
        else: 
            if typename == 'int8': # sets and saves the integer length for writing
                length = 1
            if typename == 'int16':
                length = 2
            if typename == 'int32':
                length = 4
            if typename == 'int64': 
                length = 8
            valuehex = self.hex[offset:offset+length]
            valueread = int.from_bytes(valuehex, byteorder='little') # saves the value as an integer
        return valueread

    def save(self, type: str, name: str, offset: int): # reads and saves a "stat" from a specific offset
        self.stat[name] = {} # the name of the stat (I think this might be rudundant)
        self.stat[name]["type"] = type # saves the type for writing
        self.stat[name]["offset"] = offset # saves the offset, again for writing
        self.stat[name]["value"] = self.readtype(type, offset) # reads value @ offset
        self.stat[name]['write'] = 0 # set the write stat. this is changed to 1 if the value changes
        print(f'File: New stat: {name}, {self.stat[name]['value']}, {type}, @ {offset}')
            
    def dictsearch(self, dict, typename, offset, cap=None):
        print(f'File: Searching from dict: For {typename}. From {dict}. Starting @ {offset}')
        if cap == None:
            cap = self.maxoffset
        searchoffset = offset
        while cap > searchoffset:
            search = self.readtype(typename, searchoffset)
            if search in dict.id.items():
                print(f"File: Found {search} @ {offset}")
                return searchoffset
            searchoffset += 1
        print(f"File: Failed to find {dict}: Reached {cap}")

    def intsearch(self, searchstring: int, typename: str, fromoffset: int, cap=None):
        print(f"File: Searching for {searchstring} as {typename} from {fromoffset}")
        searchoffset = fromoffset
        if cap == None:
            cap = self.maxoffset
        while cap > searchoffset: 
            search = self.readtype(typename, searchoffset)
            if search == searchstring:
                print(f"File: Found @ {searchoffset}")
                return searchoffset
            searchoffset += 1
        print(f"File: Failed to find {searchstring}: Reached {cap}")
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
                    debug(f'File: Writing {stat['value']} @ {stat['offset']} as {stat['type']}')
                    f.seek(stat['offset']) # finds the stats offset
                    if stat['type'] == 'float': # if float use struct
                        value = float(stat['value'])
                        data = struct.pack("<f", value)
                    else: # else use int_tobytes.
                        if stat['type'] == 'int8': # sets and saves the integer length for writing
                            length = 1
                        if stat['type'] == 'int16':
                            length = 2
                        if stat['type'] == 'int32':
                            length = 4
                        if stat['type'] == 'int64': 
                            length = 8
                        data = int(stat['value']).to_bytes(length, byteorder="little")
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

    def getsuites(self):
        from Suites.GhostReconBreakpoint import GR_WeaponDBEntry
        self.supportedfiles = ['GR_WeaponDBEntry']
        self.searchpatterns = {'GR_WeaponDBEntry': GR_WeaponDBEntry.read}

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
        
class SuiteReader:
    def __init__(self):
        if settings == None:
            print('SuiteReader: No Settings')
            return
        self.suitesfolder = settings.suitesfolder
        self.supportedextensions = {}
        debug(f'SuiteReader: Beginning read in {self.suitesfolder}')
        for folder in os.listdir(self.suitesfolder):
            path = os.path.join(self.suitesfolder, folder)
            mainfile = os.path.join(path, 'main.ghx')
            debug(f'Suitereader: New suite: {path}')
            debug('SuiteReader: sending to readmainfile')
            try:
                self.readmainfile(path, mainfile)
            except:
                debug('SuiteReader: No main.ghx')
                self.readwithoutmainfile(path)
            debug(f'SuiteReader: Read Suites in {path} as {self.supportedextensions}')

    def readwithoutmainfile(self, path):
        for script in os.listdir(path):
            if script.endswith('.ghx'):
                scriptpath = os.path.join(path, script)
                fileformat = script.replace('.ghx', '')
                self.supportedextensions[fileformat] = scriptpath

    def readmainfile(self, path, mainfile):
        with open(mainfile) as f:
            line = f.readline()
            while line:
                linewords = line.split(':', maxsplit=2)
                script = linewords[1].replace(' ', '')
                fileformat = linewords[0].replace('.', '')
                if script != '.ghx':
                    script = '.'.join([linewords[1], 'ghx'])
                scriptpath = os.path.join(path, script)
                self.supportedextensions[fileformat] = scriptpath
                line = f.readline()
                
class ScriptReader:
    def __init__(self, file: File, suites:SuiteReader):
        script = suites.supportedextensions[file.extension]
        with open(script) as f:
            line = f.readline()
            while line:
                if line.startswith('dependiencies:'):
                    self.readdependencies(line)
                else:
                    self.readfunction(line)
                line = f.readline()        

    def readdependencies(self, line):
        dependencies = line.split(',')

    #def readfunction(self, line):
    #    if line.startswith('@' or 'at'):

                

                        



