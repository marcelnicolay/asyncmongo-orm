# coding: utf-8
import functools
import logging
from tornado import gen
from asyncmongoorm.manager import Manager
from asyncmongoorm.session import Session
from asyncmongoorm.field import Field

__lazy_classes__ = {}

class CollectionMetaClass(type):

    def __new__(cls, name, bases, attrs):
        global __lazy_classes__
        
        # Add the document's fields to the _data
        for attr_name, attr_value in attrs.items():
            if hasattr(attr_value, "__class__") and issubclass(attr_value.__class__, Field):
                attr_value.name = attr_name
                
        new_class = super(CollectionMetaClass, cls).__new__(cls, name, bases, attrs)

        __lazy_classes__[name] = new_class
        
        new_class.objects = Manager(collection=new_class)
        
        return new_class

class Collection(object):

    __metaclass__ = CollectionMetaClass

    def __new__(cls, class_name=None, *args, **kwargs):
        if class_name:
            global __lazy_classes__
            return __lazy_classes__.get(class_name)

        return super(Collection, cls).__new__(cls, *args, **kwargs)        
        
    def __init__(self):
        self._data = {}
        

    def as_dict(self):
        items = {}
        for attr_name, attr_type in self.__class__.__dict__.iteritems():
            if isinstance(attr_type, Field):
                attr_value = getattr(self, attr_name)
                if attr_value != None:
                    items[attr_name] = attr_value
        return items    
    
    @classmethod
    def create(cls, dictionary):
        instance = cls()
        for (key, value) in dictionary.items():
            try:
                setattr(instance, str(key), value)
            except TypeError, e:
                logging.warn(e)

        return instance

    @gen.engine
    def save(self, callback=None):
        response, error = yield gen.Task(Session(self.__collection__).insert, self.as_dict(), safe=True)

        if callback:
            callback(error)

    @gen.engine
    def remove(self, callback=None):
        response, error = yield gen.Task(Session(self.__collection__).remove, {'_id': self._id})

        if callback:
            callback(error)

    @gen.engine
    def update(self, obj_data=None, callback=None):
        if not obj_data:
            obj_data = self.as_dict()

        response, error = yield gen.Task(Session(self.__collection__).update, {'_id': self._id}, obj_data, safe=True)

        if callback:
            callback(error)