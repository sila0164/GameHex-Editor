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

type_max_value = {
    'uint8': 255,
    'uint16': 65535,
    'uint24': 16777215,
    'uint32': 4294967295,
    'uint40': 1099511627775,
    'uint48': 281474976710655,
    'uint56': 72057594037927935,
    'uint64': 18446744073709551615,
    'int8': 127,
    'int16': 32767,
    'int24': 8388607,
    'int32': 2147483647,
    'int40': 549755813887,
    'int48': 140737488355327,
    'int56': 36028797018963967,
    'int64': 9223372036854775807,
}

type_min_value = {
    'uint8': 0,
    'uint16': 0,
    'uint24': 0,
    'uint32': 0,
    'uint40': 0,
    'uint48': 0,
    'uint56': 0,
    'uint64': 0,
    'int8': -128,
    'int16': -32768,
    'int24': -8388608,
    'int32': -2147483648,
    'int40': -549755813888,
    'int48': -140737488355328,
    'int56': -36028797018963968,
    'int64': -9223372036854775808,
}