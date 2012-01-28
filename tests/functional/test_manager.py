import unittest2

from asyncmongoorm.collection import Collection
from asyncmongoorm.session import Session
from asyncmongoorm.field import StringField, ObjectIdField

from tornado.ioloop import IOLoop
from tornado import testing
from bson import ObjectId

Session.create('localhost', 27017, 'asyncmongo_test')


class CollectionTest(Collection):

    __collection__ = "collection_test"

    _id = ObjectIdField()
    string_attr = StringField()
    
class ManagerTestCase(testing.AsyncTestCase):
    
    def tearDown(self):
        super(ManagerTestCase, self).tearDown()
        CollectionTest.objects.drop(callback=self.stop)
        self.wait()
        
    def get_new_ioloop(self):
        return IOLoop.instance()

    def test_find_one(self):

        collection_test = CollectionTest()
        collection_test._id = ObjectId()
        collection_test.string_attr = "string value"
        collection_test.save(callback=self.stop)
        self.wait()

        other_collection_test = CollectionTest()
        other_collection_test._id = ObjectId()
        other_collection_test.string_attr = "string value"
        other_collection_test.save(callback=self.stop)
        self.wait()

        CollectionTest.objects.find_one({'string_attr':"string value"}, callback=self.stop)
        collections_found = self.wait()

        self.assertIn(collections_found._id, (collection_test._id, other_collection_test._id))
    
    def test_find_one_not_found(self):

        CollectionTest.objects.find_one({'string_attr':"string value"}, callback=self.stop)
        collections_found = self.wait()

        self.assertEquals(None, collections_found)

    def test_find(self):
        
        collection_test = CollectionTest()
        collection_test._id = ObjectId()
        collection_test.string_attr = "string value"
        collection_test.save(callback=self.stop)
        self.wait()
        
        other_collection_test = CollectionTest()
        other_collection_test._id = ObjectId()
        other_collection_test.string_attr = "other string value"
        other_collection_test.save(callback=self.stop)
        self.wait()
        
        CollectionTest.objects.find({'string_attr':"string value"}, callback=self.stop)
        collections_found = self.wait()
        
        self.assertEquals(1, len(collections_found))
        self.assertEquals(collection_test._id, collections_found[0]._id)

    def test_find_not_found(self):
        CollectionTest.objects.find({'string_attr':"string value diff"}, callback=self.stop)
        collections_found = self.wait()

        self.assertEquals([], collections_found)
        
    def test_count(self):

        collection_test = CollectionTest()
        collection_test._id = ObjectId()
        collection_test.string_attr = "string value"
        collection_test.save(callback=self.stop)
        self.wait()

        CollectionTest.objects.count(callback=self.stop)
        count = self.wait()

        self.assertEquals(1, count)
        
    def test_can_be_find(self):

        CollectionTest.objects.drop(callback=self.stop)
        self.wait()

        collection_test = CollectionTest()
        collection_test._id = ObjectId()
        collection_test.string_attr = "string value"
        collection_test.save(callback=self.stop)
        self.wait()

        CollectionTest.objects.find({'string_attr':"string value"}, callback=self.stop)
        collections_found = self.wait()

        self.assertEquals(collection_test._id, collections_found[0]._id)

        collection_test.remove(callback=self.stop)
        self.wait()

    def test_find_distinct_values_with_distinct_command(self):
        collection_test = CollectionTest()
        collection_test._id = ObjectId()
        collection_test.string_attr = "Value A"
        collection_test.save(callback=self.stop)
        self.wait()

        collection_test = CollectionTest()
        collection_test._id = ObjectId()
        collection_test.string_attr = "Value B"
        collection_test.save(callback=self.stop)
        self.wait()

        collection_test = CollectionTest()
        collection_test._id = ObjectId()
        collection_test.string_attr = "Value A"
        collection_test.save(callback=self.stop)
        self.wait()

        collection_test = CollectionTest()
        collection_test._id = ObjectId()
        collection_test.string_attr = "Value C"
        collection_test.save(callback=self.stop)
        self.wait()

        CollectionTest.objects.distinct(key='string_attr', callback=self.stop)
        distinct_values = self.wait()

        self.assertEqual(3, len(distinct_values))
        self.assertIn("Value A", distinct_values)
        self.assertIn("Value B", distinct_values)
        self.assertIn("Value C", distinct_values)

    def test_find_distinct_values_with_distinct_command_excluding_some_values(self):
        collection_test = CollectionTest()
        collection_test._id = ObjectId()
        collection_test.string_attr = "Value A"
        collection_test.save(callback=self.stop)
        self.wait()

        collection_test = CollectionTest()
        collection_test._id = ObjectId()
        collection_test.string_attr = "Value B"
        collection_test.save(callback=self.stop)
        self.wait()

        collection_test = CollectionTest()
        collection_test._id = ObjectId()
        collection_test.string_attr = "Value A"
        collection_test.save(callback=self.stop)
        self.wait()

        collection_test = CollectionTest()
        collection_test._id = ObjectId()
        collection_test.string_attr = "Value C"
        collection_test.save(callback=self.stop)
        self.wait()

        query = {
            'string_attr': {
                '$ne': 'Value A'
            }
        }
        CollectionTest.objects.distinct(key='string_attr', query=query, callback=self.stop)
        distinct_values = self.wait()

        self.assertEqual(2, len(distinct_values))
        self.assertIn("Value B", distinct_values)
        self.assertIn("Value C", distinct_values)

    def test_execute_simple_mapreduce_return_results_inline(self):
        collections = [
            CollectionTest.create({'_id': ObjectId(), 'string_attr': 'Value A'}),
            CollectionTest.create({'_id': ObjectId(), 'string_attr': 'Value B'}),
            CollectionTest.create({'_id': ObjectId(), 'string_attr': 'Value A'}),
            CollectionTest.create({'_id': ObjectId(), 'string_attr': 'Value C'}),
            CollectionTest.create({'_id': ObjectId(), 'string_attr': 'Value D'}),
        ]
        for coll in collections:
            coll.save(callback=self.stop)
            self.wait()

        map_ = """
        function m() {
            emit(this.string_attr, 1);
        }
        """

        reduce_ = """
        function r(key, values) {
            var total = 0;
            for (var i = 0; i < values.length; i++) {
                total += values[i];
            }
            return total;
        }
        """

        CollectionTest.objects.map_reduce(map_, reduce_, callback=self.stop)
        results = self.wait()

        self.assertEquals(4, len(results))
        self.assertEquals({u'_id': u'Value A', u'value': 2.0}, results[0])
        self.assertEquals({u'_id': u'Value B', u'value': 1.0}, results[1])
        self.assertEquals({u'_id': u'Value C', u'value': 1.0}, results[2])
        self.assertEquals({u'_id': u'Value D', u'value': 1.0}, results[3])
