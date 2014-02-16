import os
import lazyconf

from lib.schema import *
from lib.prompt import *
from lib.select import *
from lib.merge import *

""" Lazyconf: Insultingly simple configuration for python applications. """

class Lazyconf():

    lazy_folder = '.lazy/'
    ignore_filename = '.gitignore'
    schema_filename = 'lazy.schema.json'
    data_filename = 'lazy.json'

    @property
    def data_file(self):
        """ Gets the full path to the file in which to save/load configured data. """
        path = os.getcwd() + '/' + self.lazy_folder
        return path + self.data_filename

    @property
    def schema_file(self):
        """ Gets the full path to the file in which to load configuration schema. """
        path = os.getcwd() + '/' + self.lazy_folder
        return path + self.schema_filename

    def __init__(self):
        """ Creates the Prompt instance, and initialises the object to hold configured data. """
        self.prompt = Prompt()
        self.data = None
    
    def add_ignore(self):
        """ Writes a .gitignore file to ignore the generated data file. """
        path = self.lazy_folder + self.ignore_filename
        
        # If the file exists, return.
        if os.path.isfile(os.path.realpath(path)):
            return None

        sp, sf = os.path.split(self.data_file)

        #Write the file.
        try:
            handle = open(path,'w')
            handle.write(sf + '\n')
        except IOError as e:
            raise e

        # Close the handle and return.
        handle.close()
        return None

    def choose_schema(self, out_file):
        """ Finds all schema templates and prompts to choose one. Copies the file to self.lazy_folder. """

        path = os.path.dirname(lazyconf.__file__) + '/schema/'
        self.prompt.header('Choose a template for your config file: ')

        i = 0
        choices = []

        for filename in os.listdir(path):
            if filename.endswith('.json'):
                try:
                    template = self._load(path + filename)
                    description = template.get('_meta.description')
                    prompt_string = str(i + 1) + '. ' + filename
                    i += 1

                    if description:
                        self.prompt.notice(prompt_string + ': ' + description)
                    else:
                        self.prompt.notice(prompt_string)

                    choices.append(template)

                except IOError as e:
                    print self.prompt.error(str(e))

        val = 0
        while val is 0 or val > i:
            val = self.prompt.int('Choice', default = 1)
            if val is 0 or val > i:
                self.prompt.error('Please choose a value between 1 and ' + str(i) + '.')
        
        schema = choices[val-1]
        
        if '_meta' in schema.data.keys():
            del(schema.data['_meta'])
        
        schema.save(out_file, as_schema=True)
        sp, sf = os.path.split(out_file)
        self.prompt.success('Saved to ' + self.lazy_folder + sf + '.')
        return schema

    def configure_data(self, data, key_string = ''):
        """ Goes through all the options in `data`, and prompts new values.
            This function calls itself recursively if it finds an inner dictionary.

            Arguments:
            data -- The dictionary to loop through. 
            key_string -- The dot-notated key of the dictionary being checked through.
        """

        # If there's no keys in this dictionary, we have nothing to do.
        if len(data.keys()) == 0:
            return

        # Split the key string by its dots to find out how deep we are.
        key_parts = key_string.rsplit('.')
        prefix = '  ' * (len(key_parts) - 1)

        # Attempt to get a label for this key string.
        label = self.data.get_label(key_string)

        # If we are have any key string or label, write the header for this section.
        if label:
            p = prefix
            if len(p) > 0:
                p += ' '
            self.prompt.header(p + '[' + label + ']')

        # Add to the prefix to indicate options on this level.
        prefix = prefix + '   '

        # If this section has an '_enabled' key, process it first, as it could enable or disable this whole section.
        if '_enabled' in data.keys():
            s = self.data.get_key_string(key_string, '_enabled')

            #Prompt whether to enable this section. Use the existing value as the default.
            data['_enabled'] = self.prompt.bool(prefix + self.data.get_label(s), None, data['_enabled'])

            # Return if this section is now disabled.
            if data['_enabled'] is False:
                return

        # Loop through the rest of the dictionary and prompt for every key. If the value is a dictionary, call this function again for the next level.
        for k, v in data.iteritems():

            # If we hit the '_enabled' key, we've already processed it (but still need it in the dictionary for saving). Ignore it.
            if k == '_enabled':
                continue
            
            # Get the type of the value at this key, and the dot-noted format of this key.
            t = type(v)
            s = self.data.get_key_string(key_string, k)

            # If the value type is a dictionary, call this function.
            if t is dict:
                self.configure_data(v, s)

            # Otherwise, parse the value.
            else:
                label = prefix + self.data.get_label(s)
                self.parse_value(data, label, s, None, v)

    def configure(self):
        """ The main configure function. Uses a schema file and an optional data file,
            and combines them with user prompts to write a new data file. """

        # Make the lazy folder if it doesn't already exist.
        path = os.getcwd() + '/' + self.lazy_folder
        if not os.path.exists(path):
            os.makedirs(path)

        schema_file = self.schema_file
        data_file = self.data_file

        # Initialise the schema and data objects.
        schema, data = Schema(), Schema()
        
        # Load the schema from a file.
        try:
            schema.load(schema_file)
        except IOError as e:

            # If we can't load the schema, choose from templates.
            self.prompt.error("Could not find schema in " + schema_file + " - Choosing from default templates...")
            schema = self.choose_schema(schema_file)
        except (Exception, ValueError) as e:
            self.prompt.error("Error: " + str(e) + " - Aborting...")
            return False
        else:
            sp, sf = os.path.split(schema_file)
            self.prompt.success('Loaded schema from ' + self.lazy_folder + sf)

        # Load the data from a file.
        try:
            data.load(data_file)
        except (Exception, IOError, ValueError) as e:
            self.prompt.error('Could not find data file. Copying from schema...')
        else:
            sp, sf = os.path.split(data_file)
            self.prompt.success('Loaded data from ' + self.lazy_folder + sf)

        # Store the internals of the schema (labels, selects, etc.) in data.
        data.internal = schema.internal

        # If we have data from a data file, merge the schema file into it.
        if data.data:

            # Create a new Merge instance using the data from the schema and data files.
            m = Merge(schema.data, data.data)
            mods = m.merge()

            for a in mods['added']:
                self.prompt.success('Added ' + a + ' to data.')

            for r in mods['removed']:
                self.prompt.error('Removed ' + r + ' from data.')

            for k,m in mods['modified']:
                self.prompt.notice('Modified ' + k + ': ' + m[0] + ' became ' + m[1] + '.' )

        # Otherwise, reference the data from the schema file verbatim.
        else:
            data.data = schema.data

        # Store the data.
        self.data = data

        # Configure the data.
        self.configure_data(data.data)

        # Save the data to the out file.
        self.data.save(self.data_file)

        self.add_ignore()

        sp, sf = os.path.split(self.data_file)
        self.prompt.success('Saved to ' + self.lazy_folder + sf + '.')

    def parse_value(self, inner_dict, label, key, value, default):
        """ Parses a single value and sets it in an inner dictionary.

            Arguments:
            inner_dict -- The dictionary containing the value to set
            label      -- The label to show for the prompt.
            key        -- The key in the dictionary to set the value for.
            value      -- The value to set. If there is a value, don't prompt for one.
            default    -- The default value in the prompt. This is taken from the schema and defines the type of the value.
        """
        t = type(default)

        if t is dict:
            return
    
        select = self.data.get_select(key)
        k = key.split('.')[-1]

        if select:
            inner_dict[k] = self.prompt.select(label, select, value, default = default)

        # If the value type is a boolean, prompt a boolean.
        elif t is bool:
            print 'as'
            inner_dict[k] = self.prompt.bool(label, value, default = default)

        # If the value is an int, prompt and int.
        elif t is int:
            inner_dict[k] = self.prompt.int(label, value, default = default)

        # If someone has put a list in data, we default it to an empty string. If it had come from the schema, it would already be a string.
        elif t is list:
            inner_dict[k] = self.prompt.prompt(label + ':', value, default = '')

        # If none of the above are true, it's a string.
        else:
            inner_dict[k] = self.prompt.prompt(label + ':', value, default = default)

    def set(self, key, value):
        """ Sets a single value in a preconfigured data file.

            Arguments:
            key -- The full dot-notated key to set the value for.
            value -- The value to set.
        """
        d = self.data.data
        keys = key.split('.')
        latest = keys.pop()
        for k in keys:
            d = d.setdefault(k, {})

        schema = Schema().load(self.schema_file)

        self.data.internal = schema.internal
        self.parse_value(d, '', key, value, schema.get(key))
        self.data.save(self.data_file)

    # Get the data for a dot-notated key.
    def get(self, key):
        """ Gets a single value from a preconfigured data file.

            Arguments:
            key -- The full dot-notated key to get the value from.
        """
        return self.data.get(key)

    def _load(self, data_file):
        """ Internal load function. Creates the object and returns it.

            Arguments:
            data_file -- The filename to load.
        """

       # Load the data from a file.
        try:
            data = Schema().load(data_file)
        except (Exception, IOError, ValueError) as e:
            raise e

        return data

    # Takes a folder and loads the data from .lazy/ in that folder.
    def load(self, data_file = None):
        """ Loads a data file and sets it to self.data.

            Arguments:
            data_file -- The filename to load.
        """

        if not data_file:
            data_file = ''
        elif data_file[-1] != '/':
            data_file += '/'

        if data_file[-6:] != self.lazy_folder:
            data_file += self.lazy_folder
        
        data_file += self.data_filename

        self.data = self._load(data_file)
        return self
