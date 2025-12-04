import struct
from db.weapondb import weapondb

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
        self.name, tempextension = os.path.splitext(self.fullname)
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
                    print (f'File: Confirmed ID Found: {name} - {id}')
                    return 'confirmed'
            print ('File: Supported fileformat found')
            return 'unknown' # returns that it is a known fileformat, but it isnt confirmed to be working
        print ('File: Unsupported file')
        return 'unsupported' # returns the file is unsupported
    
    def mount(self):
        global current
        current = self
        print(f'File: {self.name} mounted')

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
        if 'original' not in self.stat[name]: # saves the original value if it hasnt been changed before
            self.stat[name]['original'] = self.stat[name]['value'] 
        self.stat[name]['revert'] = self.stat[name]['value'] # creates a revert for the stat
        self.stat[name]['value'] = value # updates the value
        self.stat[name]['write'] = 1
        print(f'File: New value set: {name} - {value} - Old Value: {self.stat[name]['revert']}')

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
        print('File: Writing to file')
        with open(self.path, 'rb+') as f: # opens the file
            for index, statname in enumerate(self.stat): # goes through all stats
                stat = self.stat[statname]
                if stat['write'] == 1: # checks if a new value has been made
                    print(f'File: Writing {stat['value']} @ {stat['offset']} as {stat['type']}')
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
                    print(f'File: Skipping {stat}, no new value') # skips if write is not 1

                    
        
        




