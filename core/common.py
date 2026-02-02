import datetime
import os

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