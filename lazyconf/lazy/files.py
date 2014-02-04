import os, json, re
from schema_merge import SchemaMerge

class Lazyfiles():
    def __init__(self, directory = "", filename = 'lazyconf.json'):

        # Project directory and filename
        if len(directory) == 0:
            directory = '.'

        self.directory = directory
        self.filename = filename

        # Data dictionaries
        self.data = {}
        self.internal = {}

    def 