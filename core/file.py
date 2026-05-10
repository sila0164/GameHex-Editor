import struct
from core.common import dev, typelengths

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

    def saveoffset(self, type: str, title: str, offset: int, endian: str, hide: bool, removable: bool, addable: bool, newvalue: int | float | None, dict: dict | None): # reads and saves a "stat" from a specific offset
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
        self.stat[id]["newvalue"] = newvalue
        self.stat[id]["removable"] = removable
        self.stat[id]['addable'] = addable
        if dict != None:
            if not str(self.stat[id]['value']) in self.stat[id]['dict']['list_reverse']: # If the value is not on the list, add it as 'Unknown'
                self.stat[id]['dict']['list'][f'Unknown: ' + type] = str(self.stat[id]['value'])
                self.stat[id]['dict']['list_reverse'][str(self.stat[id]['value'])] = f'Unknown: ' + type
        dev(f'File.saveoffset: New stat: ID: {id} - Name: {title} - Value: {self.stat[id]['value']} - {type} @ {offset}')
            
    def dictsearch(self, dict, type, offset, endian: str, backwards:bool, cap=None) -> int:
        dev(f'File: Searching from dict for {type} from list. Starting @ {offset}')
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
                dev(f"File: Found {search} @ {searchoffset}")
                return searchoffset
            searchoffset += search_direction
        dev(f"File: Failed to find value. Reached cap: {cap} \n\n{dict}: \n\n")
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

    def write(self, new_values: dict):
        dev('File: Writing to file')
        dev(f'New values: {new_values}')
        with open(self.path, 'rb+') as f: 
            for id in new_values:
                id_as_int = int(id)
                endian = self.stat[id]['endian']
                new_value = new_values[id]
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
                        print(f'Write: Invalid type: {id['type']}. Please report as a bug.')
                    f.write(data)
                else:
                    dev(f'File: Skipping {id_as_int} - {id['title']}, no new value')
        self.hasbeenwritten = True