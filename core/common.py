devset = True
debugset = True

def dev(text):
    if devset == True:
        if text == '':
            print('')
        else:
            print(f'DEV: {text}')
            
def debug(text):
    if debugset == True:
        if text == '':
            print('')
        else:
            print(f'DEBUG: {text}')

def support_check(file, suites) -> bool:
    if file.extension in suites.supported_extensions or file.fullname in suites.supported_extensions:
        return True
    return False

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