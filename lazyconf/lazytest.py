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
        self.internal = {}

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

        # Store the internals of the schema (labels, lists, etc.) and delete it from the dictionary for merging.
        self.internal = schema.data['_internal']
        del(schema.data['_internal'])

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
        self.data.save(out_file)


c = Lazyconf()
c.configure('./lazyconf.json.schema', './lazyconf.json', './lazyconf.json')