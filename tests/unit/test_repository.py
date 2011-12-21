import unittest2
import fudge

#import asyncmongoorm.properties
from asyncmongoorm.repository import Repository

class Property(object):
    _data = None
    def __init__(self, type):
        pass
    def __get__(self, instance, owner):
        return self._data
    def __set__(self, instance, value):
        self._data = value

class MockClass(Repository):
    my_property = Property(str)
    my_status = Property(int)

    this_could_not_be_included = 1234

class RepositoryTestCase(unittest2.TestCase):
    #@fudge.with_patched_object(asyncmongoorm.properties, 'Property', Property)
    def test_get_properties_as_dict(self):
        obj = MockClass()
        obj.my_property = 'my property'
        obj.my_status = 1
        obj.instance_attribute = 'testing'

        expected_dict = {
            'my_property': 'my property',
            'my_status': 1,
        }

        self.assertEquals(expected_dict, obj.as_dict())
