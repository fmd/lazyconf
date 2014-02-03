import os, json, re
from schema_merge import SchemaMerge

class Lazyconf():
    def __init__(self, project_dir = "", filename = 'lazyconf.json'):

        # Project directory and filename
        if len(project_dir) == 0:
            project_dir = '.'

        self.project_dir = project_dir
        self.filename = filename

        # Data dictionaries
        self.data = {}
        self.internal = {}