import os
from lazyconf import Lazyconf

l = Lazyconf()
l.load(path + './lazyconf/lazyconf.json')
print l.get('db.user')
