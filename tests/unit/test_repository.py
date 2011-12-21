from datetime import datetime

import unittest2

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
    name = Property(str)
    status = Property(int)
    dictionary = Property(dict)
    created_at = Property(datetime)
    items = Property(list)

    this_could_not_be_included = 1234

class RepositoryTestCase(unittest2.TestCase):
    #@fudge.with_patched_object(asyncmongoorm.properties, 'Property', Property)
    def test_get_properties_as_dict(self):
        now = datetime.now()

        obj = MockClass()
        obj.name = 'my property'
        obj.status = 1
        obj.dictionary = {'key1': 'value1'}
        obj.created_at = now
        obj.items = [1, 2, 3]
        obj.instance_attribute = 'testing'

        expected_dict = {
            'name': 'my property',
            'status': 1,
            'dictionary': { 'key1': 'value1' },
            'created_at': now,
            'items': [1, 2, 3],
        }

        self.assertEquals(expected_dict, obj.as_dict())
