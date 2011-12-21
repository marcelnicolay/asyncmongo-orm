from datetime import datetime

import unittest2

from asyncmongoorm.repository import Repository

class Property(object):
    _data = None
    def __init__(self, type_):
        self.type = type_
    def __get__(self, instance, owner):
        return self._data
    def __set__(self, instance, value):
        if isinstance(value, self.type):
            self._data = value
        else:
            self._data = self.type(value)

class ArbitraryObject(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name

class MockClass(Repository):
    name = Property(str)
    status = Property(int)
    dictionary = Property(dict)
    created_at = Property(datetime)
    items = Property(list)
    arbitrary_object = Property(ArbitraryObject)

    this_could_not_be_included = 1234

class RepositoryTestCase(unittest2.TestCase):
    def test_get_properties_as_dict(self):
        now = datetime.now()

        obj = MockClass()
        obj.name = 'my property'
        obj.status = 1
        obj.dictionary = {'key1': 'value1'}
        obj.created_at = now
        obj.items = [1, 2, 3]
        obj.arbitrary_object = ArbitraryObject('my data')
        obj.instance_attribute = 'testing'

        expected_dict = {
            'name': 'my property',
            'status': 1,
            'dictionary': { 'key1': 'value1' },
            'created_at': now,
            'items': [1, 2, 3],
            'arbitrary_object': 'my data',
        }

        self.assertEquals(expected_dict, obj.as_dict())

    def test_create_object_from_dict(self):
        now = datetime.now()

        data = {
            'name': 'my property',
            'status': 1,
            'dictionary': { 'key1': 'value1' },
            'created_at': now,
            'items': [1, 2, 3],
            'arbitrary_object': 'my data',
        }

        created = MockClass.create(data)

        self.assertIsInstance(created, MockClass)
        self.assertEquals(created.name, 'my property')
        self.assertEquals(created.status, 1)
        self.assertEquals(created.dictionary, {'key1': 'value1'})
        self.assertEquals(created.created_at, now)
        self.assertEquals(created.items, [1, 2, 3])
        self.assertIsInstance(created.arbitrary_object, ArbitraryObject)
        self.assertEquals(str(created.arbitrary_object), 'my data')
