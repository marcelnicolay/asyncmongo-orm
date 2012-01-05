import fudge
import unittest2
from tornado import gen
from asyncmongoorm import collection
from asyncmongoorm import manager
from asyncmongoorm.field import StringField

class ManagerTestCase(unittest2.TestCase):

    @fudge.test
    @gen.engine
    def test_find_one(self):

        class CollectionTest(collection.Collection):
            __collection__ = 'some_collection'
            some_attr = StringField()

        def fake_find_one(query, callback):
            self.assertEqual(query, {'_id':1})
            callback((({'some_attr': 'some_value'},), None))

        fake_session = fudge.Fake()
        fake_session.is_callable().with_args('some_collection').returns_fake().has_attr(find_one=fake_find_one)

        with fudge.patched_context(manager, 'Session', fake_session):
            manager_object  = manager.Manager(CollectionTest)
            instance = yield gen.Task(manager_object.find_one, {'_id': 1})
            self.assertEquals('some_value', instance.some_attr)

    @fudge.test
    @gen.engine
    def test_find(self):

        class CollectionTest(collection.Collection):
            __collection__ = 'some_collection'
            some_attr = StringField()

        def fake_find(query, callback, limit):
            self.assertEqual(query, {'_id':1})
            self.assertEquals(1, limit)
            callback((([{'some_attr': 'some_value'}, {'some_attr': 'another_value'}],), None))

        fake_session = fudge.Fake()
        fake_session.is_callable().with_args('some_collection').returns_fake().has_attr(find=fake_find)

        with fudge.patched_context(manager, 'Session', fake_session):
            manager_object  = manager.Manager(CollectionTest)
            instances = yield gen.Task(manager_object.find, {'_id': 1}, limit=1)
            self.assertEquals('some_value', instances[0].some_attr)
            self.assertEquals('another_value', instances[1].some_attr)

    @fudge.test
    @gen.engine
    def test_count_without_query(self):

        fake_collection = fudge.Fake().has_attr(__collection__='some_collection')

        def fake_command(command, callback):
            self.assertEqual({"count": 'some_collection'}, command)
            callback((({'n': 10},), None))

        fake_session = fudge.Fake()
        fake_session.is_callable().returns_fake().has_attr(command=fake_command)

        with fudge.patched_context(manager, 'Session', fake_session):
            manager_object = manager.Manager(fake_collection)
            result = yield gen.Task(manager_object.count)
            self.assertEquals(10, result)

    @fudge.test
    @gen.engine
    def test_count_with_query(self):

        fake_collection = fudge.Fake().has_attr(__collection__='some_collection')

        def fake_command(command, callback):
            self.assertEqual('some_collection', command['count'])
            self.assertEqual({'tag': 'some_tag'}, command['query'])
            callback((({'n': 10},), None))

        fake_session = fudge.Fake()
        fake_session.is_callable().returns_fake().has_attr(command=fake_command)

        with fudge.patched_context(manager, 'Session', fake_session):
            manager_object = manager.Manager(fake_collection)
            result = yield gen.Task(manager_object.count, query={'tag': 'some_tag'})
            self.assertEquals(10, result)

    @fudge.test
    @gen.engine
    def test_sum(self):

        fake_collection = fudge.Fake().has_attr(__collection__='some_collection')

        def fake_command(command, callback):
            self.assertEqual('some_collection', command['group']['ns'])
            self.assertEqual({'tag': 'some_tag'}, command['group']['cond'])
            self.assertEqual({'csum': 0}, command['group']['initial'])
            self.assertEqual('function(obj,prev){prev.csum+=obj.some_field;}', command['group']['$reduce'])
            callback((({'retval': [{'csum':20}]},), None))

        fake_session = fudge.Fake()
        fake_session.is_callable().returns_fake().has_attr(command=fake_command)

        with fudge.patched_context(manager, 'Session', fake_session):
            manager_object = manager.Manager(fake_collection)
            result = yield gen.Task(manager_object.sum, {'tag': 'some_tag'}, 'some_field')
            self.assertEqual(20, result)

    @fudge.test
    @gen.engine
    def test_geo_near(self):

        fake_collection = fudge.Fake().has_attr(__collection__='some_collection')\
                                .expects('create').with_args({'key': 'value'}).returns('should_be_instance')

        def fake_command(command, callback):
            expected_command = {
                'geoNear': 'some_collection',
                'near': 'near_value',
                'query': {'tag': 'some_tag'},
                'num': 10,
                'maxDistance': 100,
                'uniqueDocs': True,
                'spherical': False
            }
            self.assertEqual(expected_command, command)
            callback((({'ok': 1, 'results':[{'obj':{'key':'value'}}]},), None))

        fake_session = fudge.Fake()
        fake_session.is_callable().returns_fake().has_attr(command=fake_command)

        with fudge.patched_context(manager, 'Session', fake_session):
            manager_object = manager.Manager(fake_collection)
            result = yield gen.Task(manager_object.geo_near,
                                        'near_value',
                                        max_distance=100,
                                        unique_docs=True,
                                        spherical=False,
                                        num=10,
                                        query={'tag': 'some_tag'})
            self.assertEquals(['should_be_instance'], result)

    @fudge.test
    @gen.engine
    def test_drop(self):

        fake_session = fudge.Fake()
        fake_session.is_callable().with_args('some_collection').returns_fake().expects('remove')

        fake_collection = fudge.Fake().has_attr(__collection__='some_collection')
        with fudge.patched_context(manager, 'Session', fake_session):
            manager_object = manager.Manager(fake_collection)
            yield gen.Task(manager_object.drop)
