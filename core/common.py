import datetime
import os
import traceback
from core.settings import settings

def dev(text):
    if settings.devdebug == True:
        if text == '':
            print('')
        else:
            print(f'DEV: {text}')

def syserror(exc_type, exc_value, exc_tb):
    print(flush=True)
    if settings.is_exe == True:
        date = datetime.datetime.now()
        date_error = (f'ERROR-{date.year}{date.month}{date.day}-{date.hour}{date.minute}{date.second}.txt')
        error_log = os.path.join(settings.root, date_error)
        with open(settings.log, 'r', encoding='utf-8') as logfile:
            error = logfile.read()
        with open(error_log, 'w', encoding="utf-8") as errorlogfile:
            errorlogfile.write(error)
            errorlogfile.write("\n" + "=" * 80 + "\n")
            errorlogfile.write(f"CRASH {datetime.datetime.now()}\n")
            traceback.print_exception(exc_type, exc_value, exc_tb, file=errorlogfile) 

def error(text):
    print(f'\n------------------------------------------------------------------\nERROR:\n{text}\n------------------------------------------------------------------\n', flush=True)
    if settings.is_exe == True:
        date = datetime.datetime.now()
        date_error = (f'ERROR-{date.year}{date.month}{date.day}-{date.hour}{date.minute}{date.second}.txt')
        error_log = os.path.join(settings.root, date_error)
        with open(settings.log, 'r', encoding='utf-8') as logfile:
            error = logfile.read()
        with open(error_log, 'w', encoding="utf-8") as errorlogfile:
            errorlogfile.write(error)
            
def debug(text):
    global settings
    if settings.debug == True:
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