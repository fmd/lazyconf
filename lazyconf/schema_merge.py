from fabric.colors import green, red

# SchemaMerge
# This class is used to merge variables in the schema dictionary into the data dictionary, without losing defaults.
# It never returns the dictionaries, as the original dictionaries are passed by reference automatically.

class SchemaMerge():
    def __init__(self, schema, data):
        self.schema = schema
        self.data = data

        # Create sets of the top level keys in both dictionaries, and the intersection between the two.
        self.set_schema = set(self.schema.keys())
        self.set_data = set(self.data.keys())
        self.intersect = self.set_schema.intersection(self.set_data)

    # Returns all top level keys which have been added to the schema.
    def added(self):
        return self.set_schema - self.intersect

    # Returns all top level keys which have been removed from the schema.
    def removed(self):
        return self.set_data - self.intersect

    # This function recursively merges all changes in the schema into the data file.
    def merge(self, schema = None, data = None, prefix = 'config'):

        if schema is None:
            schema = self.schema

        if data is None:
            data = self.data

        # Add all new keys in schema to data.
        added = self.added()
        if added:
            for a in added:
                print(green("Adding " + str(prefix + '.' + a) + " to data."))
                data[a] = schema[a]

        # Remove all keys in data that are no longer in schema.
        removed = self.removed()
        if removed:
            for r in removed:
                print(red("Removing " + str(prefix + '.' + r) + " from data."))
                del(data[r])

        # Recursively call this function until all common variables are resolved.
        intersect = self.intersect
        if intersect:
            for i in intersect:
                s = type(schema[i])
                d = type(data[i])

                # If there is a dictionary that is shared at this key by both the schema and the data, call this function again.
                if s is dict and d is dict:
                    
                    # Create a new instance of this class with the child dicts as schema and data.
                    diff = SchemaMerge(schema[i], data[i])
                    
                    # Merge the child dicts.
                    diff.merge(prefix = prefix + '.' + i)
                    
                    # Remove the created SchemaMerge
                    del(diff)

                # Otherwise if the variable type has changed, copy the variable from the schema to the data.
                elif s != d:
                    print(green("Modifying " + str(prefix + '.' + i) + " " + str(d) + " to " + str(s) ))
                    data[i] = schema[i]