import os
import json
from fabric.api import *
from fabric.colors import green, red

class Ezconf():
    def __init__(self, project_dir, filename = 'config.json'):

        ### Project directory and filename ###
        self.project_dir = project_dir
        self.filename = filename

        ### Dictionary of available database engines ###
        self.db_engines = {
            'postgres' : 'django.db.backends.postgresql_psycopg2',
            'mysql'    : 'django.db.backends.mysql',
        }

        ### Dictionary of available caching backends ###
        self.cache_backends = {
            'memcached' : 'django.core.cache.backends.memcached.MemcachedCache',
        }

        ### Skeletal config.json in dictionary form ###
        self.data = {
            'cache' : {
                'enabled'  : False,
                'backend'  : 'memcached',
                'location' : '127.0.0.1:11211',
            },

            'project' : {
                'name'        : '',
                'base_dir'    : '',
                'project_dir' : '',
            },

            'env': {
                'debug' : True,
            },

            'db' : {
                'engine' : '',
                'user'   : '',
                'name'   : '',
                'pass'   : '',
            },
        }

    ### Loading from and saving to file ###
    def load(self):
        try:
            with open(self.project_dir + '/' + self.filename) as handle:
            self.data = json.load(handle)
            handle.close()                
        except IOError:
            self.save()
            return

    def save(self):
        with open(self.project_dir + '/' + self.filename, 'w') as handle:
            json.dump(self.data, handle, indent=4)

    ### Prompt/Deprompt functions ###
    def prompt_db_engine(self, p):
        pass

    def deprompt_db_engine(self, p):
        pass

    def prompt_cache_backend(self, p):
        pass

    def depromp_cache_backend(self, p):
        pass

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

