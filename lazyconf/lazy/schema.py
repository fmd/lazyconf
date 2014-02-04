### Schema ###
### This class is used to load and store a dictionary from a config file.
### It contains methods to load data, dump data, and retrieve data from the dictionary.

class Schema():

    # Initialisation 
    def __init__(self):
        self.data = None

    # Gets a value from dot format: s.get('project.cache.backend') in dict format: self.data['project']['cache']['backend']
    def get(self, key):

        if not self.data:
            return None

        # Split the key by its dots.        
        parts = key.rsplit('.')

        # Loop through the key.
        v = self.data
        for p in parts:
            
            # Try and get the value for this section in the key.
            try:
                v = v.get(p)

            # If the key is invalid, return None rather than throwing an exception.
            except AttributeError as e:
                return None

        # If we got the value successfully, return it.
        return v

    # Loads self.data from a file.
    def load(self, path):
        data = None

        # Try and open the file, or raise an exception.
        try:
            handle = open(path)
        except IOError as e:
            raise e

        # Try to load valid JSON, or raise an exception.
        try:
            data = json.load(handle)
        except ValueError as e:
            raise e

        # Ensure that the JSON is at least a dictionary, or raise an exception.
        if type(data) is not dict:                    
            raise Exception("Invalid schema")

        # Store the dictionary.
        handle.close()
        self.data = data

    def dump(self):
        return