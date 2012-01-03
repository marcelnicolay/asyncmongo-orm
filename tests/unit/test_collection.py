import unittest2
import fudge

from asyncmongoorm.collection import Collection, __lazy_classes__
from asyncmongoorm.field import Field

class CollectionTestCase(unittest2.TestCase):
    
    def tearDown(self):
        global __lazy_classes__
        __lazy_classes__ = {}
        
    def test_can_be_set_field_name_collection(self):
        
        FakeField = fudge.Fake()
        fake_field_instance = fudge.Fake().has_attr(name=None).has_attr(__class__=Field)

        FakeField.is_callable().returns(fake_field_instance)

        class CollectionTest(Collection):
            should_be_value = FakeField()
    
        self.assertEquals(fake_field_instance.name, "should_be_value")
        
    def test_can_be_load_lazy_class(self):
        
        class CollectionTest(Collection):
            pass
        
        self.assertTrue(issubclass(Collection("CollectionTest"), CollectionTest))
        
    def test_collection_has_data_attr(self):
        
        class CollectionTest(Collection):
            pass
        
        collection_test = CollectionTest()
        self.assertTrue(hasattr(collection_test, '_data'))