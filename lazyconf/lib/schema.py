import json
from select import *

""" Schema is used to load and store a dictionary from a config file.
    It contains methods to load data, dump data, and retrieve data from the dictionary. """

class Schema():

    # Initialisation 
    def __init__(self):
        self.data = None
        self.internal = None


    # Gets a list by its dot-notated key.
    def get_select(self, k):
        if k in self.internal['selects'].keys():
            return Select(self.internal['selects'][k])
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


    #Converts the loaded dictionary for use with the Fabric API.
    def convert(self, input):
        if isinstance(input, dict):
            return {self.convert(key): self.convert(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [self.convert(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input

    # Gets a value from dot format: s.get('project.cache.backend') from dict format: self.data['project']['cache']['backend']
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
        self.data = self.convert(data)

        if '_internal' in self.data.keys():
            self.internal = self.data['_internal']
            del(self.data['_internal'])

        return self

    # Saves self.data to a file.
    def save(self, path, as_schema = False):

        if as_schema:
            self.data['_internal'] = self.internal

        # Try and save the file to the path.
        try:
            handle = open(path, 'w')
            json.dump(self.data, handle, indent = 4)

        # Raise an exception if we can't find the file.
        except IOError as e:
            raise e
        finally:
            if '_internal' in self.data.keys():
                del(self.data['_internal'])

        handle.close()