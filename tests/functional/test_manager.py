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

        self.assertEquals(collection_test._id, collections_found._id)
    
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
        other_collection_test.string_attr = "string value"
        other_collection_test.save(callback=self.stop)
        self.wait()
        
        CollectionTest.objects.find({'string_attr':"string value"}, callback=self.stop)
        collections_found = self.wait()
        
        self.assertEquals(collection_test._id, collections_found[0]._id)
        
    def test_count(self):

        collection_test = CollectionTest()
        collection_test._id = ObjectId()
        collection_test.string_attr = "string value"
        collection_test.save()

        CollectionTest.objects.count(callback=self.stop)
        count = self.wait()

        self.assertEquals(1, count)
        
    def test_can_be_find(self):

        class CollectionTest(Collection):

            __collection__ = "collection_test"

            _id = ObjectIdField()
            string_attr = StringField()

        CollectionTest.objects.drop(callback=self.stop)
        self.wait()

        collection_test = CollectionTest()
        collection_test._id = ObjectId()
        collection_test.string_attr = "string value"
        collection_test.save()

        CollectionTest.objects.find({'string_attr':"string value"}, callback=self.stop)
        collections_found = self.wait()

        self.assertEquals(collection_test._id, collections_found[0]._id)

        collection_test.remove(callback=self.stop)
        self.wait()