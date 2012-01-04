import unittest2
import fudge

from asyncmongoorm.collection import Collection, __lazy_classes__
from asyncmongoorm.field import *
from bson import ObjectId

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
        
    def test_can_get_collection_as_dict(self):
        class CollectionTest(Collection):
            string_attr = StringField()
            integer_attr = IntegerField()
            bool_attr = BooleanField()
            float_attr = FloatField()
            list_attr = ListField()
            object_attr = ObjectField()
            object_id_attr = ObjectIdField()
            unknow_object = StringField()
            
        collection_test = CollectionTest()
        collection_test.string_attr = 'string_attr'
        collection_test.integer_attr = 1
        collection_test.bool_attr = True
        collection_test.float_attr = 1.0
        collection_test.list_attr = [1,2,3]
        collection_test.object_attr = {'chave': 'valor'}
        object_id = ObjectId()
        collection_test.object_id_attr = object_id
        
        expected_dict = {
            'string_attr': 'string_attr',
            'integer_attr': 1,
            'bool_attr': True,
            'float_attr': 1.0,
            'list_attr': [1,2,3],
            'object_attr': {'chave': 'valor'},
            'object_id_attr': object_id,
        }
        
        self.assertEquals(expected_dict, collection_test.as_dict())
        
    def test_can_create_collection(self):
        object_id = ObjectId()
        object_dict = {
            'string_attr': 'string_attr',
            'integer_attr': 1,
            'bool_attr': True,
            'float_attr': 1.0,
            'list_attr': [1,2,3],
            'object_attr': {'chave': 'valor'},
            'object_id_attr': object_id,
        }
        
        class CollectionTest(Collection):
            string_attr = StringField()
            integer_attr = IntegerField()
            bool_attr = BooleanField()
            float_attr = FloatField()
            list_attr = ListField()
            object_attr = ObjectField()
            object_id_attr = ObjectIdField()
            unknow_object = StringField()
            
        object_instance = CollectionTest.create(object_dict)
        self.assertEquals('string_attr', object_instance.string_attr)
        self.assertEquals(1, object_instance.integer_attr)
        self.assertEquals(True, object_instance.bool_attr)
        self.assertEquals(1.0, object_instance.float_attr)
        self.assertEquals([1,2,3], object_instance.list_attr)
        self.assertEquals({'chave':'valor'}, object_instance.object_attr)
        self.assertEquals(object_id, object_instance.object_id_attr)
        
    def test_create_attribute_if_model_does_not_contains_field(self):
        
        class CollectionTest(Collection):
            string_attr = StringField()
            
        object_dict = {
            'string_attr': 'string_attr',
            'integer_attr': 1
        }
        
        object_instance = CollectionTest.create(object_dict)
        self.assertEquals('string_attr', object_instance.string_attr)
        self.assertEquals(1, object_instance.integer_attr)
        
    def test_ignore_attribute_with_different_field_type(self):
        
        class CollectionTest(Collection):
            string_attr = DateTimeField()
            
        object_dict = {
            'string_attr': 'duvido'
        }
        
        object_instance = CollectionTest.create(object_dict)
        self.assertIsNone(object_instance.string_attr)