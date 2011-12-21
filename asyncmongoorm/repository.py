# coding: utf-8
import logging
import functools
from datetime import datetime

from asyncmongo import Client
from bson.son import SON

from asyncmongoorm.properties import __collections__, Property
from asyncmongoorm.connection import get_database

class Repository(object):

    def as_dict(self):
        items = {}
        for attr_name, attr_type in self.__class__.__dict__.iteritems():
            if attr_name.startswith("_"):
                continue

            attr = getattr(self, attr_name)
            if attr_type.__class__.__name__ != 'Property':
                continue

            if isinstance(attr, (basestring, int, float, datetime)):
                items[attr_name] = attr

            if hasattr(attr, 'serializable'):
                items[attr.serializable] = apply(attr)

            if isinstance(attr, list):
                items[attr_name] = []
                for item in attr:
                    if isinstance(item, Repository):
                        items[attr_name] = item.as_dict()
                    else:
                        items[attr_name].append(item)

            if isinstance(attr, dict):
                items[attr_name] = attr

        return items

    @classmethod
    def create(cls, dictionary):
        instance = cls()
        for (key, value) in dictionary.items():
            setattr(instance, str(key), value)

        return instance

    @classmethod
    def find_one(cls, deferred=None, callback=None,  query={}):
        logging.debug("[MongoORM] - findone %s" % query)

        onresponse = functools.partial(cls._find_one, deferred=deferred, callback=callback)
        cls.get_collection().find_one(query, callback=onresponse)

    @classmethod
    def _find_one(cls, response, error, deferred, callback):
        logging.debug("[MongoORM] - findone SUCCESS")

        instance = None
        if response:
            instance = cls.create(response)
        
        deferred.send(instance) if deferred else callback(instance)
        
   
    @classmethod
    def find(cls, deferred=None, callback=None, query={}, **kw):
        logging.debug("[MongoORM] - find %s, %s" % (cls.__name__, query))

        onresponse = functools.partial(cls._find, deferred=deferred, callback=callback)

        cls.get_collection().find(query, callback=onresponse, **kw)

    @classmethod
    def _find(cls, result, error, deferred, callback, **kw):
        items = []
        for item in result:
            items.append(cls.create(item))

        deferred.send(items) if deferred else callback(items)

    @classmethod
    def count(cls, deferred=None, callback=None, query=None, **kw):
        onresponse = functools.partial(cls._count, deferred=deferred, callback=callback)

        db = get_database()

        command = {
            "count": cls.__collection__
        }

        if query:
            command["query"] = query

        logging.debug("[MongoORM] - counting command %s" % command)
        db.command(command, callback=onresponse)

    @classmethod
    def _count(cls, result, error, deferred, callback):
        total = int(result['n'])

        logging.debug("[MongoORM] - count result %s" % total)

        deferred.send(total) if deferred else callback(total)

    @classmethod
    def sum(cls, query=None, field=None, deferred=None, callback=None, **kw):
        onresponse = functools.partial(cls._sum, deferred=deferred, callback=callback)
        
        db = get_database()

        command = {
            "group": {
                'ns': cls.__collection__,
                'cond': query,
                'initial': {'csum': 0},
                '$reduce': 'function(obj,prev){prev.csum+=obj.'+field+';}'
            }
        }

        logging.debug("[MongoORM] - sum group command %s" % command)
        db.command(command, callback=onresponse)
        
    @classmethod
    def _sum(cls, result, error, deferred, callback):
        
        total = 0
        if result['retval']:
            total = result['retval'][0]['csum']

        logging.debug("[MongoORM] - sum result %s" % total)

        deferred.send(total) if deferred else callback(total)
        
    @classmethod
    def geo_near(cls, deferred, near, max_distance=None, num=None, spherical=None, unique_docs=None, query=None, **kw):
        onresponse = functools.partial(cls._geo_near, deferred=deferred)

        db = get_database()

        command = SON({"geoNear": cls.__collection__})

        if near != None:
            command.update({'near': near})

        if query != None:
            command.update({'query': query})

        if num != None:
            command.update({'num': num})

        if max_distance != None:
            command.update({'maxDistance': max_distance})

        if unique_docs != None:
            command.update({'uniqueDocs': unique_docs})

        if spherical != None:
            command.update({'spherical': spherical})

        logging.debug("[MongoORM] - geoNear command %s" % command)
        db.command(command, callback=onresponse)

    @classmethod
    def _geo_near(cls, result, error, deferred):
        logging.info("[MongoORM] - geoNear result ::: %s" % result['ok'])

        items = []

        if result['ok']:
            for item in result['results']:
                items.append(cls.create(item['obj']))

        deferred.send(items)

    @classmethod
    def get_collection(cls):
        db = get_database()
        return getattr(db, cls.__collection__)

    def save(self, deferred=None, callback=None):
        logging.info("[MongoORM] - save %s" % (self.__collection__))

        onresponse = functools.partial(self._save, deferred=deferred, callback=callback)
        self.get_collection().insert(self.as_dict(), safe=True, callback=onresponse)

    def _save(self, response, error, deferred, callback):        
        logging.info("[MongoORM] - save %s SUCCESS" % self.__collection__)
        
        if deferred:
            deferred.send(error)
            
        if callback:
            callback(error)

    def remove(self, deferred=None, callback=None):
        logging.info("[MongoORM] - remove %s(%s)" % (self.__collection__, self._id))

        onresponse = functools.partial(self._remove, deferred=deferred, callback=callback)
        self.get_collection().remove({'_id': self._id}, callback=onresponse)

    def _remove(self, response, error, deferred, callback):
        logging.info("[MongoORM] - remove %s(%s) SUCCESS" % (self.__collection__, self._id))
        deferred.send(error) if deferred else callback(error)

    def update(self, deferred=None, callback=None, obj_data=None):
        logging.info("[MongoORM] - update %s(%s)" % (self.__collection__, self._id))

        if not obj_data:
            obj_data = self.as_dict()

        onresponse = functools.partial(self._update, deferred=deferred, callback=callback)
        self.get_collection().update({'_id': self._id}, obj_data, safe=True, callback=onresponse)

    def _update(self, response, error, deferred, callback):        
        logging.info("[MongoORM] - update %s(%s) SUCCESS" % (self.__collection__, self._id))
        deferred.send(error) if deferred else callback(error)

    def remove_all(self):
        return self.get_collection().remove()
