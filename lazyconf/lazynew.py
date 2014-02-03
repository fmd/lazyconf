import os, json, re
from fabric.api import *
from fabric.colors import green, red

class Lazynew():
    def __init__(self, project_dir = "", filename = 'lazyconf.json'):

        # Project directory and filename
        if len(project_dir) == 0:
            project_dir = '.'

        self.project_dir = project_dir
        self.filename = filename

        # Data dictionaries
        self.data = {}
        self.internal = {}