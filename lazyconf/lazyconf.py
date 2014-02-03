import os, json, re
from fabric.api import *
from distutils.util import strtobool
from fabric.colors import green, red

class Lazyconf():

    def load_only_config(self):

        # If we're loading the config to actually serve, we can't fall back.
        self.load_data(False)

    def t(self):
        self.__configure()

    def config(self):

        # If we're configuring, load schema first for internals
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

    def __full_bool_prompt(self, v, s):
        return self.deprompt_bool(prompt(self.__get_label(s) + ' (y/n)?', default = self.prompt_bool(v), validate=r'^(y|n)$'))

    class DiffDicts():
        def __init__(self, schema, data):
            self.schema = schema
            self.data = data

            self.set_schema = set(self.schema.keys())
            self.set_data = set(self.data.keys())
            self.intersect = self.set_schema.intersection(self.set_data)

        def added(self):
            return self.set_schema - self.intersect

        def removed(self):
            return self.set_data - self.intersect

    def __cfg(self, d, key_string):

        if '_enabled' in d.keys():
            s = '.'.join([key_string,'_enabled'])
            d['_enabled'] = self.__full_bool_prompt(d['_enabled'], s)
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
                choices = '(' + ','.join(list.keys()) + ')'
                re_choices = '^(' + '|'.join(list.keys()) + ')$'.encode('string_escape');

                d[k] = self.__get_list_value(prompt(self.__get_label(s) + ' ' + choices + ':', default = self.__get_list_key(v,list), validate=re_choices), list)
            elif t is dict:
                self.__cfg(v, s)
            elif t is str or t is unicode:
                d[k] = prompt(self.__get_label(s) + ':', default = v)
            elif t is bool:
                d[k] = self.__full_bool_prompt(v, s)
            elif t is int:
                d[k] = prompt(self.__get_label(s) + ':', default = v)

    def __init__(self, project_dir, filename = 'lazyconf.json'):

        # Project directory and filename
        if len(project_dir) == 0:
            project_dir = '.'

        self.project_dir = project_dir
        self.filename = filename

        # Data dictionaries
        self.data = {}
        self.internal = {}
        self.labels = {}
        self.lists = {}

    def __recursive_dict_merge(self, schema, data, prefix = 'config'):
        diff = self.DiffDicts(schema, data)

        added = diff.added()
        if added:
            for a in added:
                print(green("Adding " + str(prefix + '.' + a) + " to data."))
                data[a] = schema[a]

        removed = diff.removed()
        if removed:
            for r in removed:
                print(red("Removing " + str(prefix + '.' + r) + " from data."))
                del(data[r])

        intersect = diff.intersect
        if intersect:
            for i in intersect:
                if type(schema[i]) is dict and type(data[i]) is dict:
                    self.__recursive_dict_merge(schema[i], data[i], prefix + '.' + i)

        del(diff)

    def __configure(self):
        path = self.project_dir + '/' + self.filename
        schema = self.__load_file(path + '.schema')
        
        if not schema:
            print(red('Falling back to default schema...'))
            schema = self.__load_file('./lazyconf.json.schema')
            if not schema:
                print(red('Could not fall back to default schema. Aborting...'))
                exit()

        data = self.__load_file(path)

        self.internal = schema['_internal']
        del(schema['_internal'])

        self.labels = self.internal['labels']
        self.lists = self.internal['lists']

        if data:
            self.__recursive_dict_merge(schema, data)

        self.data = data
        self.__cfg(self.data, 'config')
        self.save()

        # Set self.data to data and run configure.
        # Save the data file.
        pass

    def __no_configure(self):
        # Set self.data as only what was loaded in the json file. Do not fall back on schema.
        pass

    def __load_file(self, path):
        data = None
        try:
            with open(path) as handle:
                try:
                    data = json.load(handle)
                except ValueError as e:
                    print(red('Error parsing JSON: ' + str(e)))
                    return None
                if type(data) is not dict:
                    print(red('Error parsing JSON from file ' + path))
                    return None
                handle.close()
        except IOError as e:
            print(red('Could not load file: ' + str(e)))
            return None

        return data

    def load_schema(self):
        
        # Set the path to the values from __init__.
        path = self.project_dir + '/' + self.filename + '.schema'

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
            print(green("Loaded schema from " + path))

    def load_data(self, schema = True):

        # Set the path to the values from __init__.
        path = self.project_dir + '/' + self.filename

        if schema:
            self.load_schema()
        
        if not self.load_file(path):
            print(red("Could not load data from " + path + "."))
            if not schema:
                return

    def load_file(self, path, schema = False):
        try:
            with open(path) as handle:
                try:
                    self.data = json.load(handle)
                    if schema:
                        self.internal = self.data['_internal']
                        del(self.data['_internal'])

                        self.labels = self.internal['labels']
                        self.lists = self.internal['lists']

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
        if p == 'y':
            return True
        if p == 'n':
            return False
        return None

lz = Lazyconf(os.path.dirname(__file__))
lz.t()
