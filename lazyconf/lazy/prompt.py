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

    # Prints a success message.
    def success(self, msg):
        print(green(msg))

    # Prints an error message.
    def error(self, msg):
        print(red(msg))

    # Prints a notice message.
    def notice(self, msg):
        print(blue(msg))

    ### Parsing ###

    # Takes a python bool and returns it as y|n.
    def prompt_bool(self, b):
        pass

    # Takes y|n and returns a python bool.
    def deprompt_bool(self, s):
        pass

