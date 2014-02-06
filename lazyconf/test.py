import os
from lazyconf import Lazyconf

l = Lazyconf()
l.load(os.path.dirname(__file__) + '/lazyconf.json')
print l.get('db.user')
