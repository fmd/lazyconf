""" Select contains functions for getting keys from values, values from keys, and regex helpers for selecting a value from a list. """

class Select():

    # Initialisation.
    def __init__(self, d):
        self.dict = d


    # Gets the key from a value in a select.
    def get_key(self, v):
        for k,val in self.dict.iteritems():
            if v == val:
                return k
        return ""


    # Gets the value from a key in a select.
    def get_value(self, k):
        if k in self.dict.keys():
            return self.dict[k]
        return ""

    def first_choice(self):
        return sorted(self.dict.keys())[0]

    def choices(self):
        return '(' + ','.join(sorted(self.dict.keys())) + ')'


    def reg_choices(self):
        return '^(' + '|'.join(self.dict.keys()) + ')$'.encode('string_escape');