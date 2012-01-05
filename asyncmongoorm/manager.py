# coding: utf-8
import logging
from bson.son import SON
from tornado import gen
from asyncmongoorm.session import Session


class Manager(object):

    def __init__(self, collection):
        self.collection = collection
    
    @gen.engine
    def find_one(self, query, callback):
        response, error = yield gen.Task(Session(self.collection.__collection__).find_one, query=query)
        instance = self.collection.create(response) if response else None
        
        callback(instance) 
   
    @gen.engine
    def find(self, query, callback, **kw):
        result, error = yield gen.Task(Session(self.collection.__collection__).find, query=query, **kw)
        items = []
        for item in result:
            items.append(self.collection.create(item))

        callback(items)

    @gen.engine
    def count(self, query=None, callback=None):
        command = {
            "count": self.collection.__collection__
        }

        if query:
            command["query"] = query

        result, error = yield gen.Task(Session().command, command)
        
        total = int(result['n'])
        
        callback(total)
        
    @gen.engine
    def sum(self, query, field, callback):
        command = {
            "group": {
                'ns': self.collection.__collection__,
                'cond': query,
                'initial': {'csum': 0},
                '$reduce': 'function(obj,prev){prev.csum+=obj.'+field+';}'
            }
        }

        result, error = yield gen.Task(Session().command, command)
        total = 0
        if result['retval']:
            total = result['retval'][0]['csum']

        callback(total)
        
    @gen.engine
    def geo_near(self, near, max_distance=None, num=None, spherical=None, unique_docs=None, query=None, callback=None, **kw):

        command = SON({"geoNear": self.collection.__collection__})

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

        result, error = yield gen.Task(Session().command, command)
        items = []

        if result['ok']:
            for item in result['results']:
                items.append(self.collection.create(item['obj']))
        
        callback(items)

    def drop(self):
        return Session(self.collection.__collection__).remove()
