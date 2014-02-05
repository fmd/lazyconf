from fabric.api import *
from fabric.colors import green, red, blue

### Prompt ###
### This class contains several helper functions for getting data between end-user's input and a schema.Schema object.
### It also containers several formatting functions, which are currently just a convenience wrapper around printing Fabric colors.

class Prompt():

    # Initialisation
    def __init__(self):
        pass

    ### Formatting ###

    # Prints a header around a string.
    def header(self, msg):
        print(green("[" + msg + "]"))


    # Prints a success message.
    def success(self, msg):
        print(green("Success: " + msg))


    # Prints an error message.
    def error(self, msg):
        print(red("Error: " + msg))


    # Prints a notice message.
    def notice(self, msg):
        print(blue(msg))

    ### Prompts ###

    # Returns the value from a validated bool prompt.
    def bool(self, label, default = False):
        val = prompt(label + '? (y/n)', default = self.fmt_bool(default), validate = r'^(y|n)$')
        return self.defmt_bool(val)

    ### Formatting ###

    # Takes a python bool and returns it as y|n.
    def fmt_bool(self, p):
        if p is True:
            return 'y'
        if p is False:
            return 'n'
        return ''


    # Takes y|n and returns a python bool.
    def defmt_bool(self, p): 
        if p == 'y':
            return True
        if p == 'n':
            return False
        return None


