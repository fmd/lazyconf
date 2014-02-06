import os
import unittest
from lazyconf import *

# Call a configuration from this file.
def conf():
    p = os.path.dirname(__file__)
    if not p:
        p = '.'
    l = Lazyconf().configure(p  + '/schema/django.json.schema', p + '/django.json', p + '/django.json')


# Individually test the Merge class.
def merge_tests(): 
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


    pass


# Individually test the Schema class.
def schema_test():
    pass


# Individually test the Prompt class.
def prompt_test():
    pass


# Individually test the Select class.
def select_test():
    pass


# Individually test the Colors class.
def colors_test():
    pass

def test():
    merge_tests()
    schema_test()
    prompt_test()
    select_test()
    colors_test()

test()
