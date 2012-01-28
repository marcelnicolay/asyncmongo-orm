import fudge
import unittest2
from tornado import gen
from tornado import testing
from asyncmongoorm import collection
from asyncmongoorm import manager
from asyncmongoorm.field import StringField

class ManagerTestCase(testing.AsyncTestCase, unittest2.TestCase):

    @fudge.test
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
            manager_object.find_one({'_id': 1}, callback=self.stop)
            instance = self.wait()
            self.assertEquals('some_value', instance.some_attr)

    @fudge.test
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
            manager_object.find({'_id': 1}, limit=1, callback=self.stop)
            instances = self.wait()
            self.assertEquals('some_value', instances[0].some_attr)
            self.assertEquals('another_value', instances[1].some_attr)

    @fudge.test
    def test_count_without_query(self):

        fake_collection = fudge.Fake().has_attr(__collection__='some_collection')

        def fake_command(command, callback):
            self.assertEqual({"count": 'some_collection'}, command)
            callback((({'n': 10},), None))

        fake_session = fudge.Fake()
        fake_session.is_callable().returns_fake().has_attr(command=fake_command)

        with fudge.patched_context(manager, 'Session', fake_session):
            manager_object = manager.Manager(fake_collection)
            manager_object.count(callback=self.stop)
            result = self.wait()
            self.assertEquals(10, result)

    @fudge.test
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
            manager_object.count(query={'tag': 'some_tag'}, callback=self.stop)
            result = self.wait()
            self.assertEquals(10, result)

    @fudge.test
    def test_distinct(self):
        fake_collection = fudge.Fake('Collection').has_attr(__collection__='some_collection')

        def fake_command(command, callback):
            expected_command = {
                "distinct": "some_collection",
                "key": 'my_key',
                "query": {'attr': 'value'},
            }
            results = ({u'stats': {u'cursor': u'BasicCursor', u'timems': 0, u'nscannedObjects': 4, u'nscanned': 4, u'n': 4}, u'values': [u'Value A', u'Value B', u'Value C'], u'ok': 1.0},)
            self.assertEqual(expected_command, command)
            callback((results, {'error': None}))

        fake_session = fudge.Fake()
        fake_session.is_callable().returns_fake().has_attr(command=fake_command)

        distinct_results = None
        with fudge.patched_context(manager, 'Session', fake_session):
            manager_obj = manager.Manager(fake_collection)
            manager_obj.distinct(key='my_key', query={'attr': 'value'}, callback=self.stop)
            distinct_results = self.wait()

        self.assertEqual(3, len(distinct_results))

    @fudge.test
    def test_simple_map_reduce(self):
        fake_collection = fudge.Fake('Collection').has_attr(__collection__='some_collection')

        def fake_command(command, callback):
            expected_command = {
                "mapreduce": "some_collection",
                "map": 'map_fn',
                "reduce": 'reduce_fn',
                "out": {'inline': 1},
            }
            results = ({
                u'results': [
                    {u'my_key_1': u'my_data_1'},
                    {u'my_key_2': u'my_data_2'},
                    {u'my_key_3': u'my_data_3'},
                ],
                u'timeMillis': 123,
                u'counts': {u'input': 5, u'output': 3, u'emit': 5, u'reduce': 2},
                u'ok': 1,
            },)
            self.assertEquals(expected_command, command)
            callback((results, {'error': None}))

        fake_session = fudge.Fake('Session')
        fake_session.is_callable().returns_fake().has_attr(command=fake_command)

        results = None
        with fudge.patched_context(manager, 'Session', fake_session):
            manager_obj = manager.Manager(fake_collection)
            manager_obj.map_reduce("map_fn", "reduce_fn", out=None, callback=self.stop)
            results = self.wait()

        self.assertEquals(3, len(results))
        self.assertEquals({u'my_key_1': u'my_data_1'}, results[0])
        self.assertEquals({u'my_key_2': u'my_data_2'}, results[1])
        self.assertEquals({u'my_key_3': u'my_data_3'}, results[2])

    @fudge.test
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
            manager_object.sum({'tag': 'some_tag'}, 'some_field', callback=self.stop)
            result = self.wait()
            self.assertEqual(20, result)

    @fudge.test
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
            manager_object.geo_near('near_value', max_distance=100,
                                     unique_docs=True, spherical=False,
                                     num=10, query={'tag': 'some_tag'},
                                     callback=self.stop)
            result = self.wait()
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
