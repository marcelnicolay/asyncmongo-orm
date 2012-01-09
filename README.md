Asyncmongo-ORM
======================

Asyncmongo-ORM is a object-relation mapping for asyncmongo. [AsyncMongo](http://github.github.com/bitly/asyncmongo) is an asynchronous library for accessing mongo which is built on the tornado ioloop.

<<<<<<< HEAD
asyncmongoorm is currently in version 0.2.0 and supports the following features:

 * Map an collection
 * Map fields of type (object_id, object, list, boolean, datetime, integer, string)
 * Session facade to connection client
 * Support to find, find_one, count, sum, geo_near and command
 * Signals for pre_save, post_save, pre_remove, post_remove, pre_update, post_update

=======
>>>>>>> d7fe05264d8990dee928c59c5c246df85f47894a
Installation
-----------------

Installing: `pip install asyncmongoorm`

<<<<<<< HEAD
Common Usage
=======
Usage
>>>>>>> d7fe05264d8990dee928c59c5c246df85f47894a
--------------

    from asyncmongoorm.collection import Collection
    from asyncmongoorm.session import Session
    from asyncmongoorm.field import StringField, ObjectIdField, BooleanField, DateTimeField
    
    from datetime import datetime
    import tornado.web
    from tornado import gen

<<<<<<< HEAD
    # create a new collection
    class User(Collection):
    
        # collection name
        __collection__ = "user"
        
        # map fields
=======
    class User(Collection):
        __collection__ = "user"
        
>>>>>>> d7fe05264d8990dee928c59c5c246df85f47894a
        _id = ObjectIdField()
        name = StringField()
        active = BooleanField()
        created = DateTimeField()
        
<<<<<<< HEAD
    # create asyncmongo session client
    Session.create('localhost', 27017, 'asyncmongo_test') 
=======
    Session.create('localhost', 27017, 'asyncmongo_test') # create asyncmongo session client
>>>>>>> d7fe05264d8990dee928c59c5c246df85f47894a
    
    class Handler(tornado.web.RequestHandler):

        @tornado.web.asynchronous
        @gen.engine
        def get(self):
            user = User()
            user.name = "User name"
            user.active = True
            user.created = datetime.now()

            yield gen.Task(user.save)

            # update date
            user.name = "New name"
            yield gen.Task(user.update)

            # find one object
            user_found = yield gen.Task(User.objects.find_one, user._id)
            
            # find many objects
            new_user = User()
            new_user.name = "new user name"
            new_user.user.active = True
            new_user.created = datetime.now()
            
            users_actives = yield gen.Task(User.objects.find, {'active': True})
            
            users_actives[0].active = False
            yield gen.Task(users_actives[0].save)

            # remove object
            yield gen.Task(user_found.remove)

<<<<<<< HEAD
Signals Usage
-------------------

    from asyncmongoorm.collection import Collection
    from asyncmongoorm.session import Session
    from asyncmongoorm.field import StringField, ObjectIdField, BooleanField, DateTimeField
    from asyncmongoorm.signal import pre_save, receiver

    import tornado.web
    from tornado import gen

    # create a new collection
    class User(Collection):

        # collection name
        __collection__ = "user"
    
        # map fields
        _id = ObjectIdField()
        name = StringField()
        active = BooleanField()
        created = DateTimeField()
    
    @receiver(pre_save, User)
    def set_object_id(sender, instance):
        if not instance._id:
            instance._id = ObjectId()
    
    # create asyncmongo session client
    Session.create('localhost', 27017, 'asyncmongo_test') 

    class Handler(tornado.web.RequestHandler):

        @tornado.web.asynchronous
        @gen.engine
        def get(self):
            user = User()
            user.name = "User name"
            user.active = True
            user.created = datetime.now()

            yield gen.Task(user.save)
            
For more examples, view [functional tests](https://github.com/marcelnicolay/asyncmongo-orm/tree/master/tests/functional)

=======
>>>>>>> d7fe05264d8990dee928c59c5c246df85f47894a
Requirements
------------
The following three python libraries are required

* [pymongo](http://github.com/mongodb/mongo-python-driver) version 1.9+ for bson library
* [tornado](http://github.com/facebook/tornado)
* [asyncmongo](http://github.github.com/bitly/asyncmongo)

Issues
------

Please report any issues via [github issues](https://github.com/marcelnicolay/asyncmongo-orm/issues)