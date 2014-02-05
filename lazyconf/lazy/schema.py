import json

### Schema ###
### This class is used to load and store a dictionary from a config file.
### It contains methods to load data, dump data, and retrieve data from the dictionary.

class Schema():

    # Initialisation 
    def __init__(self):
        self.data = None
        self.internal = None


    # Gets the key from a value in a list.
    def get_list_key(self, v, list):
        for k,val in list.iteritems():
            if v == val:
                return k
        return ""


    # Gets the value from a key in a list.
    def get_list_value(self, k, list):
        if k in list.keys():
            return list[k]
        return ""


    # Gets a list by its dot-notated key.
    def get_list(self, k):
        if k in self.internal['lists'].keys():
            return self.internal['lists'][k]
        return None


    # Gets a label by its dot-notated key.
    def get_label(self, label):
        if label in self.internal['labels'].keys():
            return self.internal['labels'][label]
        return label


    # Adds 'val' to 'key' in dot notation.
    def get_key_string(self, key, val):
        if key:
            return '.'.join([key, val])
        return val


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

        if '_internal' in self.data.keys():
            self.internal = self.data['_internal']
            del(self.data['_internal'])


    # Saves self.data to a file.
    def save(self, path):

        # Try and save the file to the path.
        try:
            handle = open(path, 'w')
            json.dump(self.data, handle, indent = 4)

        # Raise an exception if we can't find the file.
        except IOError as e:
            raise e

        handle.close()