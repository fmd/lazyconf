import re
from colors import Colors
### Prompt ###
### This class contains several helper functions for getting data to and from the end-user's input and a schema.Schema object.

class Prompt():

    # Initialisation
    def __init__(self):
        pass

    ### Formatting ###

    # Prints a header around a string.
    def header(self, msg):
        print(Colors.header + msg + Colors.end)


    # Prints a success message.
    def success(self, msg):
        print(Colors.success + msg + Colors.end)


    # Prints an error message.
    def error(self, msg):
        print(Colors.error + msg + Colors.end)


    # Prints a notice message.
    def notice(self, msg):
        print(Colors.blue + msg + Colors.end)


    # The prompt string method.
    # This method heavily models how it works in Fabric.
    def string(self, label, default='', validate=None):
        
        p = label + ' ' + '[%s]' % str(default).strip() + ' '
        value = None
        while value is None:

            # Get the raw input.
            value = raw_input(p) or default
            if validate:

                # Attempt to validate the string if it's callable.
                if callable(validate):
                    try:
                        value = validate(value)
                    except Exception, e:

                        # If the regex fails, loop.
                        value = None
                        print("Validation failed for the following reason:")
                        print(indent(e.message) + '\n')

                # Attempt to validate it if it's not callable.
                else:
                    if not validate.startswith('^'):
                        validate = r'^' + validate

                    if not validate.endswith('$'):
                        validate += r'$'

                    result = re.findall(validate, value)
                    if not result:
                        print("Regular expression validation failed: '%s' does not match '%s'\n" % (value, validate))

                        # If the regex fails, loop.
                        value = None

        return value

    ### Prompts ###

    # Returns the value from a validated int prompt.
    def int(self, label, default = 0):
        val = self.string(label + ' (int):', default = str(default), validate = r'^[0-9]+$')
        return int(val)


    # Returns the value from a validated bool prompt.
    def bool(self, label, default = False):
        val = self.string(label + ' (y/n):', default = self.fmt_bool(default), validate = r'^(y|n)$')
        return self.defmt_bool(val)


    # Returns the value from a validated select prompt.
    def select(self, label, select, default = ""):
        deft = select.get_key(default)
        if not deft:
            deft = select.first_choice()
        return select.get_value(self.string(label + ' ' + select.choices() + ':', default = deft, validate = select.reg_choices()))


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