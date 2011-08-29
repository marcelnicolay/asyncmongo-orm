# coding: utf-8
#!/usr/bin/env python

from asyncmongo import Client

from morm.propertie import __collections__
from morm import get_database

from datetime import datetime
from torneira import settings

import logging
import functools
      
class Repository(object):
        
    def as_dict(self):
        items = {}
        for attrname in dir(self):
            if attrname.startswith("_"):
                continue

            attr = getattr(self, attrname)
            if isinstance(attr, (basestring, int, float, datetime)):
                items[attrname] = attr
            if hasattr(attr, 'serializable'):
                items[attr.serializable] = apply(attr)

            if isinstance(attr, list):
                if len(attr) > 0 and isinstance(attr[0], dict):
                    items[attrname] = attr
                else:
                    items[attrname] = [x.as_dict() for x in attr]
            
            if isinstance(attr, dict):
                items[attrname] = attr

        return items
    
    @classmethod
    def create(cls, dictionary):
        instance = cls()
        for (key, value) in dictionary.items():
            setattr(instance, str(key), value)
        
        return instance

    @classmethod
    def find_one(cls, deferred,  query={}):
        logging.debug("[MongoORM] - findone %s" % query)

        onresponse = functools.partial(cls._find_one, deferred=deferred)
        cls.get_collection().find_one(query, callback=onresponse)

    @classmethod
    def _find_one(cls, response, error, deferred):
        logging.debug("[MongoORM] - findone %s SUCCESS" % response)

        if response:
            instance = cls.create(response)
            deferred.send(instance)
        else:
            deferred.send(False)
   
    @classmethod
    def find(cls, deferred, query, **kw):
        logging.debug("[MongoORM] - find %s, %s" % (cls.__name__, query))

        onresponse = functools.partial(cls._find, deferred=deferred)
        cls.get_collection().find(query, callback=onresponse, **kw)
        
    @classmethod
    def _find(cls, result, error, deferred, **kw):
        items = []
        for item in result:
            items.append(cls.create(item))

        deferred.send(items)
        
    @classmethod
    def count(cls, deferred, **kw):
        logging.debug("[MongoORM] - counting %s" % cls.__name__)
        onresponse = functools.partial(cls._count, deferred=deferred)
        
        db = get_database()
        db.command({"count": cls.__collection__}, callback=onresponse)
        
    @classmethod
    def _count(cls, result, error, deferred):
        total = int(result['n'])
        
        logging.debug("[MongoORM] - count result %s" % total)
        
        deferred.send(total)
        
    @classmethod
    def get_collection(cls):
        db = get_database()
        return getattr(db, cls.__collection__)

    def save(self, deferred):
        logging.info("[MongoORM] - save %s" % (self.__collection__))
        
        onresponse = functools.partial(self._save, deferred=deferred)
        self.get_collection().insert(self.as_dict(), safe=True, callback=onresponse)


    def _save(self, response, error, deferred):        
        logging.info("[MongoORM] - save %s SUCCESS" % self.__collection__)
        deferred.send(error)

        
    def remove(self, deferred):
        logging.info("[MongoORM] - remove %s(%s)" % (self.__collection__, self._id))
        
        onresponse = functools.partial(self._remove, deferred=deferred)
        self.get_collection().remove({'_id': self._id}, callback=onresponse)
        
    def _remove(self, response, error, deferred):
        logging.info("[MongoORM] - remove %s(%s) SUCCESS" % (self.__collection__, self._id))
        deferred.send(error)
        
        
    def update(self, deferred):
        logging.info("[MongoORM] - update %s(%s)" % (self.__collection__, self._id))
        
        onresponse = functools.partial(self._update, deferred=deferred)
        self.get_collection().update({'_id': self._id}, self.as_dict(), safe=True, callback=onresponse)

    def _update(self, response, error, deferred):        
        logging.info("[MongoORM] - update %s(%s) SUCCESS" % (self.__collection__, self._id))
        deferred.send(error)

    def remove_all(self):
        return self.get_collection().remove()

