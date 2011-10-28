# coding: utf-8
#!/usr/bin/env python

from asyncmongoorm import defer

from tornado.ioloop import IOLoop

import unittest
import functools
import time
    
class FindTestCase(unittest.TestCase):
    
    def test_can_be_find(self):
        
        print ">>A"
        
        self.find()
        print ">>B"
        
        
    def find_items(self, deferred):
        
        print "find items"
        
        deferred.send("ITEM")
    
    @defer.inlineCallbacks
    def find(self, deferred, **kw):
        
        print "exec>>"
        
        advs = yield self.find_items(deferred=deferred)
        print ">>%s" % advs
