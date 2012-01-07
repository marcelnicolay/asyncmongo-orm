from tornado import testing
from tornado.ioloop import IOLoop
from asyncmongoorm import signal
from asyncmongoorm.session import Session
from asyncmongoorm.collection import Collection
from asyncmongoorm.field import StringField, ObjectId, ObjectIdField

Session.create('localhost', 27017, 'asyncmongo_test')

class SignalTestCase(testing.AsyncTestCase):

    def get_new_ioloop(self):
        return IOLoop.instance()

    def test_save_sends_pre_save_signal_correctly_and_I_can_handle_with_it(self):

        class CollectionTest(Collection):

            __collection__ = "collection_test"

            _id = ObjectIdField()
            string_attr = StringField()

        @signal.receiver(signal.pre_save, CollectionTest)
        def collection_pre_save_handler(sender, instance):
            instance.string_attr += " updated"

        collection_test = CollectionTest()
        collection_test._id = ObjectId()
        collection_test.string_attr = "should be string value"
        collection_test.save()

        CollectionTest.objects.find_one(collection_test._id, callback=self.stop)

        collection_found = self.wait()
        self.assertEquals("should be string value updated", collection_found.string_attr)

    def test_save_sends_post_save_signal_correctly_and_I_can_handle_with_it(self):

        class CollectionTest(Collection):

            __collection__ = "collection_test"

            _id = ObjectIdField()
            string_attr = StringField()

        @signal.receiver(signal.post_save, CollectionTest)
        def collection_post_save_handler(sender, instance):
            CollectionTest.objects.find_one(collection_test._id, callback=self.stop)
            collection_found = self.wait()
            self.assertEquals(instance.string_attr, collection_found.string_attr)

        collection_test = CollectionTest()
        collection_test._id = ObjectId()
        collection_test.string_attr = "should be string value"
        collection_test.save()

