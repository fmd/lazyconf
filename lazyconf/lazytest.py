from lazy.prompt import *
from lazy.schema import *
from lazy.merge import *

### Lazyconf ###
### Our main class. These functions should all be chainable through Fabric for use on a remote server.

class Lazyconf():

    # Initialisation.
    def __init__(self):
        self.prompt = Prompt()
        self.data = None
        

    # Goes through all the options in the data file, and prompts new values.
    def configure_data(self, data, key_string = ''):
        
        # If there's no keys in this dictionary, we have nothing to do.
        if len(data.keys()) == 0:
            return

        key_parts = key_string.rsplit('.')
        prefix = "--" * (len(key_parts) - 1)

        label = self.data.get_label(key_string)
        prefix = prefix + "-- "

        if label:
            header = self.prompt.header(label)

        if '_enabled' in data.keys():
            s = self.data.get_key_string(key_string, '_enabled')
            data['_enabled'] = self.prompt.bool(prefix + self.data.get_label(s), data['_enabled'])
            if data['_enabled'] is False:
                return

        for k, v in data.iteritems():
            if key_string == '_internal':
                return

            if k == '_enabled':
                continue
            
            t = type(v)
            s = self.data.get_key_string(key_string, k)

            list = self.data.get_list(s)
            if list:
                choices = '(' + ','.join(list.keys()) + ')'
                re_choices = '^(' + '|'.join(list.keys()) + ')$'.encode('string_escape');

                data[k] = self.data.get_list_value(prompt(prefix + self.data.get_label(s) + ' ' + choices + ':', default = self.data.get_list_key(v,list), validate=re_choices), list)
            elif t is dict:
                self.configure_data(v, s)
            elif t is str or t is unicode:
                data[k] = prompt(prefix + self.data.get_label(s) + ':', default = v)
            elif t is bool:
                data[k] = self.prompt.bool(prefix + self.data.get_label(s))
            elif t is int:
                data[k] = prompt(prefix + self.data.get_label(s) + ':', default = v)


    # Loads the schema from a schema file.
    def configure(self, schema_file, data_file, out_file):

        # Initialise the schema and data objects.
        schema, data = Schema(), Schema()
        
        # Load the schema from a file.
        try:
            schema.load(schema_file)
        except Exception as e:

            # If we can't load the schema, abort.
            self.prompt.error(str(e) + ". Aborting...")
            return
        else:
            self.prompt.success("Loaded schema from " + schema_file)

        # Load the data from a file.
        try:
            data.load(data_file)
        except Exception as e:
            self.prompt.error(str(e))

            # If we can't load the data, we can continue from the schema.
            # If the data file path was entered incorrectly, we can abort.
            cont = self.prompt.bool("Continue from schema", True)
            if not cont:
                self.prompt.error("Aborting...")
                return
        else:
            self.prompt.success("Loaded data from " + data_file)

        # Store the internals of the schema (labels, lists, etc.) in data.
        data.internal = schema.internal

        # If we have data from a data file, merge the schema file into it.
        if data.data:
            m = Merge(schema.data, data.data)
            mods = m.merge()
            for a in mods['added']:
                print(green("Added " + a + " to data."))

            for r in mods['removed']:
                print(red("Removed " + r + " from data."))

            for k,m in mods['modified']:
                print(blue("Modified " + k + ": " + m[0] + " became " + m[1] + "." ))

        # Otherwise, reference the data from the schema file verbatim.
        else:
            data.data = schema.data

        self.data = data
        self.configure_data(data.data)
        self.data.save(out_file)

c = Lazyconf()
c.configure('./lazyconf.json.schema', './lazyconf.json', './lazyconf.json')