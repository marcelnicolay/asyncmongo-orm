class PropertyDict(dict):
    def __getattr__(self, name):
        if name.startswith("_"):
            return dict.__getattr__(self, name)
        return self[name]

class Property(object):
    def __init__(self, type=None, doc=None, default=None):
        self.type = type
        self.default = default
        self.name = None

        self.__doc__ = doc

    def __get__(self, instance, owner):
        if instance is None:
            return self

        value = instance._data.get(self.name)
        if value is None:
            return self.default

        return value

    def __set__(self, instance, value):
        if self.type and not isinstance(value, self.type) and value is not None:
            try:
                value = self.type(value)            
            except ValueError:
                raise(ValueError("type of %s must be %s" % (self.name, self.type)))

        instance._data[self.name] = value

__lazy_classes__ = {}

class CollectionMetaClass(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(CollectionMetaClass, cls).__new__

        # Add the document's fields to the _data
        for attr_name, attr_value in attrs.items():
            if hasattr(attr_value, "__class__") and issubclass(attr_value.__class__, Property):
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

    