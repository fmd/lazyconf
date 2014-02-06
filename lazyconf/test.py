import os
from lazyconf import Lazyconf

l = Lazyconf()
l.load('./lazyconf/lazyconf.json')
print l.get('db.user')
