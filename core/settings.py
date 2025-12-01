from core.localization import languages
import os
import sys
import json


class Settings:
    def __init__(self):
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

        # Loads Settings file if it exists
        if os.path.exists(self.settingsfile):
            print('Importing settings from file')
            with open(self.settingsfile, "r", encoding='utf-8') as f:
                self.settings = json.load(f)
        
        # Creates a new if it doesn't
        else:
            print('No settings file, creating new with defaults')
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

        # gets suites from files
        #self.getsuites()

        # Creates backupfolder if there isnt any, if the user wants backups
        if self.wantbackups == True:
            print("Creating backup folder if there isn't any")
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
            print(f"Changed: {name} to: {value}")
            success = True
        if isinstance(value, str) and setting[1] == 'color': # checks the string is a valid rgb hex value
            if isinstance(value, str) and value.startswith("#") and len(value) == 7:
                int(value[1:], 16) 
                print(f'Changed: {name} to: {value}')
                success = True
        if isinstance(value, str) and setting[1] == 'language': # checks if its a supported language
            if value in languages:
                print(f'Changed language to: {value}')
                success = True
        if success == True: # If any checks were succesful it sets the value and saves to settings.json
            setting[0] = value
            with open(self.settingsfile, "w") as f:
                json.dump(self.settings, f, indent=4)
                return True
        else: # if checks were unsuccessful it return False
            print(f"Could not change: {name} to: {value} as it was not a: {self.settings[name][1]}")
            return False

settings = None

def initsettings() -> bool:
    global settings
    print('Initializing settings')
    try:
        settings = Settings()
        settingsinit = True
        print('Settings Initialized')
    except Exception as e:
        print('Could not initialize settings:', e)
        settingsinit = False
    return settingsinit
