# coding: utf-8
#!/usr/bin/env python

import functools    
import logging

class Deferred(object):
    
    def __init__(self):
        self.function = None
        
    def setFunction(self, function):
        self.function = function
        
    def send(self, result):

        logging.debug("[Defer] - send result %s to function %s" % (result, self.function.__name__))

        try:
            self.function.send(result)
        except StopIteration:
            self.function.close()
        
def inlineCallbacks(fn):
    
    def wrapper(*args, **kwargs):
        
        deferred = Deferred()

        function_generator = fn(deferred=deferred, *args, **kwargs)
        deferred.setFunction(function_generator)
        
        function_generator.send(None)


    return wrapper