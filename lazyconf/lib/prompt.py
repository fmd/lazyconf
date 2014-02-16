import re
from colors import Colors

""" Prompt contains all the methods for parsing and returning input. """

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


    def validate_prompt(self, value, validate):
        if validate:
            if callable(validate):
                try:
                    value = validate(value)
                except Exception, e:

                    # If the regex fails, loop.
                    value = None
                    self.error("Validation failed for the following reason:")
                    self.error(e.message + '\n')

            # Attempt to validate it if it's not callable.
            else:
                if not validate.startswith('^'):
                    validate = r'^' + validate

                if not validate.endswith('$'):
                    validate += r'$'

                result = re.findall(validate, value)
                if not result:
                    self.error("Regular expression validation failed: '%s' does not match '%s'\n" % (value, validate))

                    # If the regex fails, loop.
                    value = None

        return value

    # The prompt string method.
    # This method heavily models how it works in Fabric.
    def prompt(self, label, value=None, default='', validate=None):
        
        p = label + ' ' + '[%s]' % str(default).strip() + ' '
        prompt_string = None

        if not value:
            value = None
            while value is None:
                prompt_string = raw_input(p) or default
                value = self.validate_prompt(prompt_string, validate)
        else:
            value = self.validate_prompt(value, validate)

        return value

    ### Prompts ###

    # Returns the value from a validated int prompt.
    def int(self, label, value=None, default = 0):
        ret = self.prompt(label + ' (int):', value=value, default = str(default), validate = r'^[0-9]+$')
        return int(ret)


    # Returns the value from a validated bool prompt.
    def bool(self, label, value=None, default = False):
        ret = self.prompt(label + ' (y/n):', value=value, default = self.fmt_bool(default), validate = r'^(y|n)$')
        return self.defmt_bool(ret)


    # Returns the value from a validated select prompt.
    def select(self, label, select, value=None, default = ""):
        dflt = select.get_key(default)
        if not dflt:
            dflt = select.first_choice()

        return select.get_value(self.prompt(label + ' ' + select.choices() + ':', value = value, default = dflt, validate = select.reg_choices()))

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