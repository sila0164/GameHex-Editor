

def typeread(offset, typelength, hex):
    start = offset
    end = offset + typelength
    readhex = hex[start:end]
    read = int.from_bytes(readhex, byteorder="little")
    return read  

def dictsearch(dict, typelength, offset, cap=None):
    if cap == None:
        cap = main.file.maxoffset
    searchoffset = offset
    while cap > searchoffset:
        search = typeread(searchoffset, typelength)
        if search in dict.items():
            print(f"Found {search} @ {offset}")
            return searchoffset
        searchoffset += 1
    print(f"Failed to find {dict}")

def typesearch(searchstring, typelength, offset, cap=None):
    #print(f"Searching for {searchstring} as {type} from {offset}")
    searchoffset = offset
    if cap == None:
        cap = main.file.maxoffset
    while cap > searchoffset: 
        search = typeread(searchoffset, typelength)
        if search == searchstring:
            return searchoffset
            #print(f"Found {name} - {searchstring} @ {offset}")
        searchoffset += 1
    print(f"Failed to find {searchstring}")