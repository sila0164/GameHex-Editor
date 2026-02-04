import os
import sys
import json
import time

def cleanline(line: str) -> str:
    if '#' in line:
        line_split = line.split('#') # Allaws for comments with # in lines, ignores everything after '#'
        line = line_split[0]
    line = line.strip().replace('&enter&', '\n')
    return line

def findline(f, linenumber: int):
    f.seek(0)
    for lines in range(linenumber):
        f.readline()

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
            print(f'Language list: {filename}: Could not read name on line 1:\n{line}\nSkipping list...')
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
                print(f'Language list: Reached end at line {line_number}')
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
                print(f'Language List: {name} line {line_number}: incorrect syntax:\n{line}\nIgnoring line...')
            line_number += 1
            line = f.readline()
    return name, returndict

def getlocalizations(localization_folder_path: str) -> tuple[bool, dict]:
    localizations = {}
    print(localization_folder_path)
    for language in os.listdir(localization_folder_path):
        if language.endswith('.ghex'):
            language_path = os.path.join(localization_folder_path, language)
            language_name, language_list = readlist(language_path, start=None, language=True)
            if language_name != '':
                localizations[language_name] = language_list
                print(f'Localization: Loaded language: {language_name}')

    if len(localizations) == 0:
        print('Localization: No languages found!')
        return False, localizations
    return True, localizations

class Settings:
    def __init__(self):

        self.is_exe = getattr(sys, 'frozen', False) # Check to see if is running as exe or script

        if self.is_exe == True:
            self.root = os.path.dirname(sys.executable)
        else:
            self.root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.chdir(self.root)  
        sys.path.append(self.root)

        if self.is_exe == True:
            sys.stdout = open("Log.txt", "w", encoding="utf-8") # Log file creation
            self.log = os.path.join(self.root, "Log.txt") 

        self.suitesfolder = os.path.join(self.root, 'Suites') # Checks for suites folder and creates it if it doesnt exist
        if not os.path.exists(self.suitesfolder):
            os.makedirs(self.suitesfolder, exist_ok=False)

        self.localizationfolder = os.path.join(self.root, 'Localization') # Checks for localization folder and creates it if it doesnt
        if not os.path.exists(self.localizationfolder):
            os.makedirs(self.localizationfolder, exist_ok=False)
            print('Settings: No Localizations. Please add at least one localization .ghex file to the "Localization"-folder.')
            sys.exit()

        # Default settings in case settings file cant be read
        self.language: str = 'English'
        self.background: str = '#222222'
        self.text: str = '#EEEEEE'
        self.border: str = '#AAAAAA'
        self.highlight: str = '#666666'
        self.accent: str = '#444444'
        self.darkaccent: str = '#333333'
        self.treeview: bool = True
        #self.firstlaunch: bool = True
        #self.wantbackups: bool = False
        self.openfile: bool = False
        self.debug: bool = False
        self.hidehidden: bool = True
        self.devdebug: bool = False
        print('Settings: Default settings initialized')

        self.getlocalization()
        
        try:
            self.readsettings()
            print('Settings: Settings loaded from file')
        except Exception as e:
            print('Settings: Could not read file, force-creating new settings.json')
            try:
                self.readsettings(force=True)
            except Exception as e:
                print(f'Settings: Could not force-create settings: {e}')
                sys.exit
            
    def getlocalization(self):
        # Reading the Localization folder
        succes, self.languages = getlocalizations(self.localizationfolder)
        if succes == False:
            print('Settings: No languages found, shutting down. Please make sure there is at least one .ghex localization file in the Localization folder.')
            sys.exit()

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
            'treeview': [True, 'bool'],
            #'firstlaunch': [True, 'bool'],
            'language': ['English', 'language'],
            #'wantbackups': [False, 'bool'], 
            'debug': [False, 'bool'],
            'hidehidden': [True, 'bool'],
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
        self.treeview: bool = self.settings['treeview'][0]
        #self.firstlaunch: bool = self.settings['firstlaunch'][0]
        #self.wantbackups: bool = self.settings['wantbackups'][0]
        #self.openfile: bool = False 
        self.debug: bool = self.settings['debug'][0]
        self.hidehidden: bool = self.settings['hidehidden'][0]
        self.devdebug: bool = self.settings['devdebug'][0]

        if self.debug == True:
            print('Settings: Debug messages are enabled')
        
        if self.devdebug == True:
            print('Settings: Devdebug messages are enabled. (These are primarily for debugging GameHex, not for scripts.)')
            print(f'Settings: Current Language: {self.language}')

        # Creates backupfolder if there isnt any, if the user wants backups
        #if self.wantbackups == True:
        #    print("Settings: Creating backup folder if there isn't any")
        #    os.makedirs('Backups', exist_ok=True)

        return True
    
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

start = time.time()
print('Settings: Getting settings')
settings = Settings()
end = time.time()
print(f'Settings: Settings Initialized. Time elapsed: {end - start} seconds')


