# coding: utf-8
import logging
import functools
from bson.son import SON
from tornado import gen
from asyncmongoorm.session import Session


class Manager(object):

    def __init__(self, collection):
        self.collection = collection
    
    @classmethod
    @gen.engine
    def find_one(cls, query, callback):
        logging.debug("[MongoORM] - findone %s" % query)

        response, error = yield gen.Task(cls.get_collection().find_one, query=query)
        instance = cls.create(response) if response else None
        
        callback(instance) 
   
    @classmethod
    @gen.engine
    def find(cls, query, callback, **kw):
        logging.debug("[MongoORM] - find %s, %s" % (cls.__name__, query))

        result, error = yield gen.Task(cls.get_collection().find, query=query, **kw)
        items = []
        for item in result:
            items.append(cls.create(item))

        callback(items)

    @classmethod
    @gen.engine
    def count(cls, query=None, callback=None, **kw):
        db = Session()

        command = {
            "count": cls.__collection__
        }

        if query:
            command["query"] = query

        logging.debug("[MongoORM] - counting command %s" % command)
        result, error = yield gen.Task(db.command, command)
        
        total = int(result['n'])
        
        callback(total)
        
    @classmethod
    @gen.engine
    def sum(cls, query=None, field=None, callback=None, **kw):
        db = Session()

        command = {
            "group": {
                'ns': cls.__collection__,
                'cond': query,
                'initial': {'csum': 0},
                '$reduce': 'function(obj,prev){prev.csum+=obj.'+field+';}'
            }
        }

        logging.debug("[MongoORM] - sum group command %s" % command)
        result, error = yield gen.Task(db.command, command)
        total = 0
        if result['retval']:
            total = result['retval'][0]['csum']

        logging.debug("[MongoORM] - sum result %s" % total)

        callback(total)
        
    @classmethod
    @gen.engine
    def geo_near(cls, near, max_distance=None, num=None, spherical=None, unique_docs=None, query=None, callback=None, **kw):
        db = Session()

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
        result, error = yield gen.Task(db.command, command)
        items = []

        if result['ok']:
            for item in result['results']:
                items.append(cls.create(item['obj']))
        
        callback(items)

    @classmethod
    def get_collection(cls):
        db = Session()
        return getattr(db, cls.__collection__)

    @gen.engine
    def save(self, callback=None):
        logging.info("[MongoORM] - save %s" % (self.__collection__))

        response, error = yield gen.Task(self.get_collection().insert, self.as_dict(), safe=True)

        if callback:
            callback(error)

    @gen.engine
    def remove(self, callback=None):
        logging.info("[MongoORM] - remove %s(%s)" % (self.__collection__, self._id))

        onresponse = functools.partial(self._remove, deferred=deferred, callback=callback)
        response, error = yield gen.Task(self.get_collection().remove, {'_id': self._id})

        if callback:
            callback(error)

    @gen.engine
    def update(self, obj_data=None, callback=None):
        logging.info("[MongoORM] - update %s(%s)" % (self.__collection__, self._id))

        if not obj_data:
            obj_data = self.as_dict()

        onresponse = functools.partial(self._update, deferred=deferred, callback=callback)
        response, error = yield gen.Task(self.get_collection().update, {'_id': self._id}, obj_data, safe=True)

        if callback:
            callback(error)

    @classmethod
    def remove_all(cls):
        return cls.get_collection().remove()
