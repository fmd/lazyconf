import os 
import unittest
import lazyconf

from lib.schema import *
from lib.prompt import *
from lib.select import *
from lib.merge import *

# A function to be called from the setup entrypoint.
def conf():
    lazyconf.Lazyconf().configure()

if __name__ == '__main__':
    conf()