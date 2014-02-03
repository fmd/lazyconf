import os
import json
from fabric.api import *
from distutils.util import strtobool
from fabric.colors import green, red

class Lazyconf():

    def config(self):
        self.load()
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

    def __get_label(self, l):
        if l in self.data['_internal']['labels'].keys():
            return self.data['_internal']['labels'][l]
        return l

    def __cfg(self, d, key_string):

        if '_enabled' in d.keys():
            s = '.'.join([key_string,'_enabled'])
            d['_enabled'] = self.deprompt_bool(prompt(self.__get_label(s), default = self.prompt_bool(d['_enabled'])))
            if d['_enabled'] is False:
                return

        for k, v in d.iteritems():
            if key_string == 'config._internal':
                return

            if k == '_enabled':
                continue
            
            t = type(v)
            s = '.'.join([key_string,k])

            if t is dict:
                self.__cfg(v, s)
            elif t is str or t is unicode:
                d[k] = prompt(self.__get_label(s), default = v)
            elif t is bool:
                d[k] = self.deprompt_bool(prompt(self.__get_label(s), default = self.prompt_bool(v)))
            elif t is int:
                d[k] = prompt(self.__get_label(s), default = v)

    def __init__(self, project_dir, filename = 'lazyconf.json'):

        ### Project directory and filename ###
        if len(project_dir) == 0:
            project_dir = '.'

        self.project_dir = project_dir

        self.filename = filename

        self.data = {}

        self.labels = {}

        self.lists = {}

    def load(self, path = None):
        if not self.load_file(path):
            if not self.load_file(path, True):
                if not self.load_file('./' + self.filename, True):
                    print(red("Fatal: Could not load JSON file, schema, or local schema. Aborting..."))
                    exit()

        self.labels = self.data['_internal']['labels']
        self.lists = self.data['_internal']['lists']

    def load_file(self, path = None, schema = False):
        if path is None:
            path = self.project_dir + '/' + self.filename
        if schema:
            path += '.schema'
        try:
            with open(path) as handle:
                print(green("Loading JSON from " + path))
                try:
                    self.data = json.load(handle)
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
    def prompt_db_engine(self, p):
        for key, engine in self.db_engines.iteritems():
            if p == engine:
                return key
        return ''

    def deprompt_db_engine(self, p):
        engine = self.db_engines[p]
        if len(engine) > 0:
            return engine
        return None

    def prompt_cache_backend(self, p):
        for key, backend in self.cache_backends.iteritems():
            if p == backend:
                return key
        return ''

    def deprompt_cache_backend(self, p):
        engine = self.cache_backends[p]
        if len(engine) > 0:
            return engine
        return None

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
