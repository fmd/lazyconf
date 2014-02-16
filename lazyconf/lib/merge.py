
""" Merge used to merge variables in the schema dictionary into the data dictionary, without losing defaults.
    It never returns the dictionaries, as the original dictionaries are passed by reference automatically.
    The schema dictionary is never be modified by this class. """

class Merge():

    # Initialisation creates sets of the top level keys in both dictionaries, and the intersection between the two.
    def __init__(self, schema, data):
        self.schema = schema
        self.data = data

        # Create the sets.
        self.set_schema = set(self.schema.keys())
        self.set_data = set(self.data.keys())
        self.intersect = self.set_schema.intersection(self.set_data)
        

    # Returns all top level keys which have been added to the schema.
    def added(self):
        return self.set_schema - self.intersect


    # Returns all top level keys which have been removed from the schema.
    def removed(self):
        return self.set_data - self.intersect

    # This method recursively merges all changes in the schema into the data file.
    def merge(self, schema = None, data = None, prefix = None):
        
        # If there's no prefix yet, don't add a '.'
        p = ''
        if prefix:
            p = prefix + '.'
        
        # Create the dictionary to be returned.
        mods = {
            'added'   : [], # []string
            'removed' : [], # []string
            'modified': []  # [](string,(type,type))
        }

        if schema is None:
            schema = self.schema

        if data is None:
            data = self.data

        # Add all new keys in schema to data.
        added = self.added()
        if added:
            for a in added:
                mods['added'].append(p + a)
                data[a] = schema[a]

        # Remove all keys in data that are no longer in schema.
        removed = self.removed()
        if removed:
            for r in removed:
                mods['removed'].append(p + r)
                del(data[r])

        # Recursively call this method until all common variables are resolved.
        intersect = self.intersect
        if intersect:
            for i in intersect:
                s = type(schema[i])
                d = type(data[i])

                # If there is a dictionary that is shared at this key by both the schema and the data, call this method again.
                if s is dict and d is dict:
                    
                    # Create a new instance of this class with the child dicts as schema and data.
                    diff = Merge(schema[i], data[i])
                    
                    # Merge the child dicts.
                    add_mods = diff.merge(prefix = p + i)

                    # Update our return dict.
                    mods['added'] += add_mods['added']
                    mods['removed'] += add_mods['removed']
                    mods['modified'] += add_mods['modified']
                    
                    # Remove the created Merge.
                    del(diff)

                # Otherwise if the variable type has changed, copy the variable from the schema to the data.
                elif s != d:
                    
                    # Here, we process lists into empty strings.
                    if s is list:
                            data[i] = ""

                    # If we're not dealing with a list, process normally.
                    else: 
                        # Add this to the 'modified' list.
                        m = (p + i, (str(d),str(s)))
                        mods['modified'].append(m)

                        # Copy the value from the schema to the data.
                        data[i] = schema[i]

        # Return the dictionary of modifications.
        return mods