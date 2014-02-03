import os
import json
from fabric.api import *
from distutils.util import strtobool
from fabric.colors import green, red

class Lazyconf():

    def load_only_config(self):

        # If we're loading the config to actually serve, we can't fall back.
        self.load_data(False)

    def config(self):

        # If we're configuring, fall back on schema if the file doesn't exist.
        self.load_data(True)
        self.__cfg(self.data, 'config')
        self.save()

    def save_schema(self):
        d = self.data
        self.__sv_schema(d)

    def __sv_schema(self, d):
        for k,v in d.iteritems():
            if t is dict:
                self.__sv_schema(d)
            elif t is bool:
                v = False
            elif t is int:
                v = 0
            else:
                v = ''
        return

    def __get_list(self, k):
        if k in self.lists.keys():
            return self.lists[k]
        return None

    def __get_list_value(self, k, l):
        if k in l.keys():
            return l[k]
        return ""

    def __get_list_key(self, v, l):
        for k,val in l.iteritems():
            if v == val:
                return k
        return ""

    def __get_label(self, l):
        if l in self.labels.keys():
            return self.labels[l]
        return l

    def __cfg(self, d, key_string):

        if '_enabled' in d.keys():
            s = '.'.join([key_string,'_enabled'])
            d['_enabled'] = self.deprompt_bool(prompt(self.__get_label(s) + ' (y/n)?', default = self.prompt_bool(d['_enabled'])))
            if d['_enabled'] is False:
                return

        for k, v in d.iteritems():
            if key_string == 'config._internal':
                return

            if k == '_enabled':
                continue
            
            t = type(v)
            s = '.'.join([key_string,k])

            list = self.__get_list(s)
            if list:
                d[k] = self.__get_list_value(prompt(self.__get_label(s) + '(' + ','.join(list.keys()) + ')' + ':', default = self.__get_list_key(v,list)), list)
            elif t is dict:
                self.__cfg(v, s)
            elif t is str or t is unicode:
                d[k] = prompt(self.__get_label(s) + ':', default = v)
            elif t is bool:
                d[k] = self.deprompt_bool(prompt(self.__get_label(s) + ' (y/n)?', default = self.prompt_bool(v)))
            elif t is int:
                d[k] = prompt(self.__get_label(s) + ':', default = v)

    def __init__(self, project_dir, filename = 'lazyconf.json'):

        ### Project directory and filename ###
        if len(project_dir) == 0:
            project_dir = '.'

        self.project_dir = project_dir

        self.filename = filename

        self.data = {}

        self.labels = {}

        self.lists = {}

    def load_schema(self):
        
        # Set the path to the values from __init__.
        path = self.project_dir + '/' + self.filename

        # If we can't find a schema file in that folder, load the default schema.
        if not self.load_file(path, True):
            print(red("Could not load schema from " + path + ". Falling back to default..."))

            bkp_path = './' + self.filename

            # If we can't find the default schema, we cannot continue.
            if not self.load_file(bkp_path, True):
                print(red("Fatal: Could not load default schema from " + bkp_path + ". Aborting..."))
                exit()
            else:
                print(green("Loaded default schema."))
        else:
            print(green("Loaded schema from " + path + ".schema"))

    def load_data(self, fallback = True):

        # Set the path to the values from __init__.
        path = self.project_dir + '/' + self.filename

        # If we can't find the file in the folder and we're falling back ot schema, call load_schema.
        if not self.load_file(path):
            if fallback:
                self.load_schema()
            else:
                print(red("Fatal: Could not load schema from " + path + ". Aborting..."))
                exit()

    def load_file(self, path, schema = False):
        if schema:
            path += '.schema'
        try:
            with open(path) as handle:

                try:
                    self.data = json.load(handle)
                    self.labels = self.data['_internal']['labels']
                    self.lists = self.data['_internal']['lists']
                except ValueError as e:
                    print(red('Error parsing JSON: ' + str(e)))
                    return None
                if type(self.data) is not dict:
                    print(red('Error parsing JSON from file ' + path))
                    return None
                handle.close()
        except IOError as e:
            print(red('Could not load file: ' + str(e)))
            return None

        return True

    def save(self, d = None, f = None):
        if not d:
            d = self.data
        if not f:
            f = self.filename
        try:
            with open(self.project_dir + '/' + f, 'w') as handle:
                json.dump(d, handle, indent=4)
        except IOError as e:
            print(red('Could not save file: ' + str(e)))
            exit()
        else:
            print(green('Saved data to file: ' + f))

    ### Prompt/Deprompt functions ###
    def prompt_bool(self, p):
        if p is True:
            return 'y'
        if p is False:
            return 'n'
        return ''

    def deprompt_bool(self, p): 
        if p.lower() in ['y','yes','true']:
            return True
        if p.lower() in ['n','no','false']:
            return False
        return None

lz = Lazyconf(os.path.dirname(__file__))
lz.config()
