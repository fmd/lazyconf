from lazy.prompt import *
from lazy.schema import *
from lazy.merge import *

### Lazyconf ###
### Our main class. These functions should all be chainable through Fabric for use on a remote server.

class Lazyconf():

    # Initialisation.
    def __init__(self):
        self.prompt = Prompt()

    # Loads the schema from a schema file.
    def configure(self, schema_file, data_file):

        # Initialise the schema and data objects.
        schema, data = Schema(), Schema()
        
        # Load the schema from a file.
        try:
            schema.load(schema_file)
        except Exception as e:
            self.prompt.error(str(e) + ". Aborting...")
            return

        else:
            self.prompt.success("Successfully loaded schema from " + schema_file)

        # Load the data from a file.
        try:
            data.load(data_file)
        except Exception as e:
            self.prompt.error(str(e))

            # If we can't load the data file, we can continue from the schema.
            # If the data file path was entered incorrectly, we can abort.
            cont = self.prompt.bool("Continue from schema", True)
            if not cont:
                self.prompt.error("Aborting...")
                return
        else:
            self.prompt.success("Successfully loaded data from " + data_file)

c = Lazyconf()
c.configure('./lazyconf.json.schema', './lazyconf.json')