import os
from lazyconf import Lazyconf

l = Lazyconf()
path = os.path.dirname(__file__)
if len(path) == 0:
    path = '.'

l.load(path + '/lazyconf.json')
print l.get('db.user')
