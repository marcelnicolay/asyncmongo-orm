import unittest2

from asyncmongoorm.collection import Collection
from asyncmongoorm.session import Session
from asyncmongoorm.field import StringField, ObjectIdField

from tornado.ioloop import IOLoop
from tornado import testing
from bson import ObjectId

Session.create('localhost', 27017, 'asyncmongo_test')

class CollectionTestCase(testing.AsyncTestCase):
    
    def get_new_ioloop(self):
        return IOLoop.instance()

    def test_can_be_save(self):
        
        class CollectionTest(Collection):
            
            __collection__ = "collection_test"
        
            _id = ObjectIdField()
            string_attr = StringField()
            
        collection_test = CollectionTest()
        collection_test._id = ObjectId()
        collection_test.string_attr = "should be string value"
        collection_test.save()
        
        CollectionTest.objects.find_one(collection_test._id, callback=self.stop)
        
        collection_found = self.wait()
        self.assertEquals(collection_test.string_attr, collection_found.string_attr)