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
        
        if 'Collection' in [b.__name__ for b in bases]:
            global __lazy_classes__
            __lazy_classes__[name] = new_class

#        cls.objects = Manager(collection=cls)
        
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
        
    """
    def as_dict(self):
        items = {}
        for attr_name, attr_type in self.__class__.__dict__.iteritems():
            if attr_name != '_id' and attr_name.startswith("_"):
                continue

            attr = getattr(self, attr_name)
            if attr_type.__class__.__name__ != 'Field':
                continue

            if attr is None:
                items[attr_name] = None
            elif isinstance(attr, (basestring, int, float, datetime, dict, ObjectId)):
                items[attr_name] = attr
            elif hasattr(attr, 'serializable'):
                items[attr.serializable] = apply(attr)
            elif isinstance(attr, list):
                items[attr_name] = []
                for item in attr:
                    if isinstance(item, Repository):
                        items[attr_name] = item.as_dict()
                    else:
                        items[attr_name].append(item)
            else:
                items[attr_name] = str(attr)

        return items

    @classmethod
    def create(cls, dictionary):
        instance = cls()
        for (key, value) in dictionary.items():
            try:
                setattr(instance, str(key), value)
            except AttributeError:
                logging.warn("Attribute %s.%s could not be set" % (instance.__class__.__name__, key))

        return instance
        
    """
