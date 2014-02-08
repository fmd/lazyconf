import os 
import unittest
import lazyconf

from lib.schema import *
from lib.prompt import *
from lib.select import *
from lib.merge import *

class LazyTests(unittest.TestCase): 

    # Individually test the Merge class.
    def test_merge(self):
        schema = {
            "present1" : True,
            "present2" : "foo",
            "present3" : 12,
            "present4" : {
                "p1" : 1,
                "p2" : "too",
                "p3" : True
            },

            "added1" : False,
            "added2" : "bar",
            "added3" : 24,
            "added4" : [1,2,3,4,5],


            "modified1" : {
                "a" : 1,
                "b" : True,
                "c" : "baz"
            },

            "modified2" : [5,4,3,2,1],
            "modified3" : [24,45,23,87,4],
        }

        data = {
            "present1" : False,
            "present2" : "",
            "present3" : 0,
            "present4" : {
                "p1" : 0,
                "p2" : "",
                "p3" : False
            },

            "modified1" : "foobar",
            "modified2" : 12345,
            "modified3" : True,
            "modified4" : True,

            "removed1" : "remo",
            "removed2" : 23,
            "removed3" : {
                "all" : "of",
                "us" : "will",
                "be" : "removed"
            }
        }

        merge = Merge(schema, data)
        mods = merge.merge()

        return


    # Individually test the Schema class.
    def test_schema(self):
        p = os.path.dirname(lazyconf.__file__)
        if not p:
            raise Exception("Could not find local path.")

        s = Schema()

        val = s.get('db.engine')

        with self.assertRaises(ValueError):
            s.load(p + '/schema/test/invalid.json')

        with self.assertRaises(IOError):
            s.load(p + '/schema/test/noexist.json')

        with self.assertRaises(Exception):
            s.load(p + '/schema/test/noobject.json')

        s.load(p + '/schema/test/valid.json')

        select = s.get_select('db.engine')
        select = s.get_select('db.noexist')
        label = s.get_label('db.engine')
        label = s.get_label('db.noexist')

        key1 = s.get_key_string('','one')
        key2 = s.get_key_string('one','two')

        val = s.get('db.engine')
        val = s.get('db.engine.noexist')

        s.save('/dev/null')

        with self.assertRaises(IOError):
            s.save('/noexist/does_not_exist')

        return


    # Individually test the Prompt class.
    def test_prompt(self):
        p = Prompt()

        p.header("Testing.")
        p.success("Testing.")
        p.error("Testing.")
        p.notice("Testing.")

        return


    # Individually test the Select class.
    def test_select(self):
        return

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(LazyTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
