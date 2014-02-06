import os
from lazyconf import Lazyconf

l = Lazyconf()
l.load(os.path.dirname(__file__) + '/skel/lazyconf.json.skel')
print l.get('db.user')