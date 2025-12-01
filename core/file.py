import struct
from db.weapondb import weapondb
from core.settings import settings

#Should never import from anything other than db and settings

current = None # This is where the currently opened file is saved and accessed

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
        self.name, tempextension = os.path.splitext(path)
        self.extension = tempextension.lstrip('.') 
        self.stat = {} # a dictionary of all added stats for each file

    def __repr__(self): #all data contained in the class
        return f'Name: {self.name} \nId: {self.id}\nLength: {self.maxoffset}\n\nStats:\n{self.stat}\n\nFull bytes:\n{self.hex}'
    
    def hassupport(self):
        #if self.extension in settings.supportedfiles: # Checks if file is supported
        if self.extension == 'GR_WeaponDBEntry':
            for index, name in enumerate(weapondb): # checks for confirmed support
                id = weapondb[name]
                if self.id == id:
                    print ('Confirmed ID Found')
                    return 'confirmed'
            print ('Supported fileformat found')
            return 'unknown' # returns that it is a known fileformat, but it isnt confirmed to be working
        print ('Unsupported file')
        return 'unsupported' # returns the file is unsupported
    
    def mount(self):
        global current
        current = self


    def readtype(self, typename: str, offset: int):
        print(typename)
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
        self.stat[name]["value"] = self.readtype(type, offset)
            
    def dictsearch(self, dict, typename, offset, cap=None):
        if cap == None:
            cap = self.maxoffset
        searchoffset = offset
        while cap > searchoffset:
            search = self.readtype(typename, searchoffset)
            if search in dict.id.items():
                print(f"Found {search} @ {offset}")
                return searchoffset
            searchoffset += 1
        print(f"Failed to find {dict}: Reached {cap}")

    def intsearch(self, searchstring: int, typename: str, fromoffset: int, cap=None):
        #print(f"Searching for {searchstring} as {type} from {offset}")
        searchoffset = fromoffset
        if cap == None:
            cap = self.maxoffset
        while cap > searchoffset: 
            search = self.readtype(typename, searchoffset)
            if search == searchstring:
                return searchoffset
            #print(f"Found {name} - {searchstring} @ {offset}")
            searchoffset += 1
        print(f"Failed to find {searchstring}: Reached {cap}")
        return 0

    def getstats(self):
        return self.stat # returns the full stat dictionary 

    def changevalue(self, name:str, value): # changes current value for a stat which will be written if wanted
        if 'original' not in self.stat[name]: # saves the original value if it hasnt been changed before
            self.stat[name]['original'] = self.stat[name]['value'] 
        self.stat[name]['revert'] = self.stat[name]['value'] # creates a revert for the stat
        self.stat[name]['value'] = value # updates the value

    def revert(self):
        for index, stat in enumerate(self.stat): # goes through all stats
            if 'revert' in stat: # only reverts stats with a revert value
                stat['value'] = stat['revert']
    
    def revertoriginal(self):
        for index, stat in enumerate(self.stat): # goes through all stats
            if 'original' in stat: # only reverts stats with a original value
                stat['revert'] = stat['value'] # updates revert
                stat['value'] = stat['original'] # sets the value to original

    def write(self):
        with open(self.path, 'rb+') as f: # opens the file
            for index, stat in enumerate(self.stat): # goes through all stats
                if 'revert' in stat: # checks if a new value has been made
                    f.seek(stat['offset']) # finds the stats offset
                    if stat['type'] == 'float': # if float use struct
                        data = struct.pack("<f", stat['value'])
                    else: # else use int_tobytes. The length of the int is saved when reading the stat
                        length = stat['typelength']
                        data = int(stat['value']).to_bytes(length, byteorder="little")
                    f.write(data) # writes the value to a given offset

                    
        
        




