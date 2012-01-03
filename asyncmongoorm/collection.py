# coding: utf-8
from asyncmongoorm.field import Field

__lazy_classes__ = {}

class CollectionMetaClass(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(CollectionMetaClass, cls).__new__

        # Add the document's fields to the _data
        for attr_name, attr_value in attrs.items():
            if hasattr(attr_value, "__class__") and issubclass(attr_value.__class__, Field):
                attr_value.name = attr_name

        new_class = super_new(cls, name, bases, attrs)

        if attrs.has_key("__collection__"):
            global __lazy_classes__
            __lazy_classes__[name] = new_class

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