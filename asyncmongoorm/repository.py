# coding: utf-8
from asyncmongo import Client

from asyncmongoorm.properties import __collections__
from asyncmongoorm.connection import get_database

from datetime import datetime

from bson.son import SON

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
        logging.debug("[MongoORM] - findone SUCCESS")

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
    def count(cls, deferred, query=None, **kw):
        onresponse = functools.partial(cls._count, deferred=deferred)

        db = get_database()

        command = {
            "count": cls.__collection__
        }

        if query:
            command["query"] = query

        logging.debug("[MongoORM] - counting command %s" % command)
        db.command(command, callback=onresponse)

    @classmethod
    def _count(cls, result, error, deferred):
        total = int(result['n'])

        logging.debug("[MongoORM] - count result %s" % total)

        deferred.send(total)

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

    def update(self, deferred, obj_data=None):
        logging.info("[MongoORM] - update %s(%s)" % (self.__collection__, self._id))

        if not obj_data:
            obj_data = self.as_dict()

        onresponse = functools.partial(self._update, deferred=deferred)
        self.get_collection().update({'_id': self._id}, obj_data, safe=True, callback=onresponse)

    def _update(self, response, error, deferred):        
        logging.info("[MongoORM] - update %s(%s) SUCCESS" % (self.__collection__, self._id))
        deferred.send(error)

    def remove_all(self):
        return self.get_collection().remove()
