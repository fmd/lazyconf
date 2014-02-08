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
    sp_get.add_argument('-k', '--key',
                        help='The key to retrieve.', dest='key')

    return parser.parse_args()

def console():
    command_dict = parse().__dict__
    command = command_dict['command']

    l = lazyconf.Lazyconf()

    if command == 'get':
        try:
            l.load()
        except:
            exit()
        r = l.get(command_dict['key'])
        if r:
            print r
        exit()

    elif command == 'config':
        l.configure()
       
# Call the console function if we call this file directly.
if __name__ == '__main__':
    console()
