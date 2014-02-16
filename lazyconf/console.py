import argparse
import lazyconf

from lib.schema import *
from lib.prompt import *
from lib.select import *
from lib.merge import *

# A function to be called from the setup entrypoint.
def parse():
    parser = argparse.ArgumentParser(prog='lazyconf')
    sp = parser.add_subparsers(dest='command')

    sp_config = sp.add_parser('config', help='Run the configurator.')
    
    sp_get = sp.add_parser('get', help='Gets the value for a specific key in the configuration.')
    sp_set = sp.add_parser('set', help='Sets the value for a specific key in the configuration.')
    sp_parse = sp.add_parser('parse', help='Parses and saves previously set keys')
    
    sp_get.add_argument('-k', '--key',
                        help='The key to retrieve.', dest='key', required=True)
    sp_set.add_argument('-k', '--key',
                        help='The key to set for.', dest='key', required=True)
    sp_set.add_argument('-v', '--value',
                        help='The value to set.', dest='value', required=True)
    
    return parser.parse_args()

def get(l, key):
    try:
        l.load()
    except:
        exit()
    
    r = l.get(key)
    if r:
        print r
    exit()

def set(l, key, value):
    try:
        l.load()
    except Exception as e:
        raise  e

    try:
        l.set(key, value)
    except Exception as e:
        raise e

    exit()

def console():
    command_dict = parse().__dict__
    command = command_dict['command']

    l = lazyconf.Lazyconf()

    if command == 'get':
        key = command_dict['key']
        get(l, key)
    elif command == 'config':
        l.configure()
    elif command == 'set':
        key = command_dict['key']
        value = command_dict['value']
        set(l, key, value)
       
# Call the console function if we call this file directly.
if __name__ == '__main__':
    console()
