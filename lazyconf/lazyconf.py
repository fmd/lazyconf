import os, json, re
from fabric.api import *
from fabric.colors import green, red, blue
from schema_merge import SchemaMerge
# TODO: Prompt falling back to default schema.

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

    def __get_label(self, l ,prefix = ""):
        if l in self.labels.keys():
            return prefix + self.labels[l]
        return prefix + l

    def __full_bool_prompt(self, v, s):
        return self.deprompt_bool(prompt(s + '? (y/n)', default = self.prompt_bool(v), validate=r'^(y|n)$'))

    def __cfg(self, d, key_string):
        if len(d.keys()) == 0:
            return

        key_parts = key_string.rsplit('.')
        prefix = "--" * (len(key_parts) - 1)
        label = self.__get_label(key_string)
        if label is key_string:
            label = key_parts[-1]

        header = prefix + " [" + label  + "]"
        prefix = prefix + "-- "

        print(green(header))

        if '_enabled' in d.keys():
            s = '.'.join([key_string,'_enabled'])
            d['_enabled'] = self.__full_bool_prompt(d['_enabled'], self.__get_label(s, prefix))
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

                d[k] = self.__get_list_value(prompt(self.__get_label(s, prefix) + ' ' + choices + ':', default = self.__get_list_key(v,list), validate=re_choices), list)
            elif t is dict:
                self.__cfg(v, s)
            elif t is str or t is unicode:
                d[k] = prompt(self.__get_label(s, prefix) + ':', default = v)
            elif t is bool:
                d[k] = self.__full_bool_prompt(v, self.__get_label(s, prefix))
            elif t is int:
                d[k] = prompt(self.__get_label(s, prefix) + ':', default = v)

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

    def __configure(self):
        path = self.project_dir + '/' + self.filename
        schema = self.__load_file(path + '.schema')
        
        if not schema:
            fall = self.__full_bool_prompt("", "Fall back to default schema")
            if not fall:
                print(red("Did not fall back to default schema. Aborting..."))
                exit()

            schema = self.__load_file('./lazyconf.json.schema')
            if not schema:
                print(red('Could not fall back to default schema. Aborting...'))
                exit()
            else:
                print(green('Loaded default schema.'))
        else:
            print(green('Loaded schema.'))

        self.internal = schema['_internal']
        del(schema['_internal'])

        self.labels = self.internal['labels']
        self.lists = self.internal['lists']

        data = self.__load_file(path)

        if data:
            print(green("Loaded data."))
            d = SchemaMerge(schema, data)
            mods = d.merge()
            for a in mods['added']:
                print(green("Added " + a + " to data."))

            for r in mods['removed']:
                print(red("Removed " + r + " from data."))

            for k,m in mods['modified']:
                print(blue("Modified " + k + ": " + m[0] + " became " + m[1] + "." ))

            self.data = data
        else:
            self.data = schema
            
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