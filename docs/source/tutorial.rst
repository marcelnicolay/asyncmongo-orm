========
Tutorial
========

This tutorial is meant to introduce you to the basic concepts of using
Asyncmongo-ORM using an example application. The example application is a
simple user database where people could fill in their information and
register themselves.


Getting started
===============

  * Ensure that an instance of MongoDB is running in an accessible
    location. This tutorial assumes that such an instance is running on the
    localhost.


Defining our Collection 
=======================

A `MongoDB Collection <http://www.mongodb.org/display/DOCS/Collections>`_
is the rough equivalent of a table in a relational database. Though
MongoDB collections are schemaless documents in them usually have a
similar structure. This "similar structure" could be defined as a
:class:`~asyncmongoorm.collection.Collection`.

In this example application we define the structure of Users collection
with the required :py:mod:`~asyncmonogoorm.field` (s) ::


    class User(Collection):
        __collection__ = "user"
        
        _id = ObjectIdField()
        name = StringField()
        active = BooleanField()
        created = DateTimeField()


Connecting to the Database
==========================

A connection to the MongoDB database needs to be established before
Asyncmongo-ORM can manage collections or do any other operations. A
connection is established using a :class:`~asyncmongoorm.session.Session`
object ::

    from asyncmongoorm.session import Session
    Session.create('localhost', 27017, 'asyncmongo_test')


Creating a new document
=======================

A new document can be created in the collection by creating an instance of
the Collection, assigning values to the fields and then calling the save
method ::

    new_user = User()
    new_user.name = "New user"
    new_user.active = True
    new_user.save()


A new instance would also be created from a dictionary (for example from a
Form handler in your web application)::

    >>> new_user = User.create({'name': 'Sharoon'})
    >>> new_user.name
    u'Sharoon'
    >>> new_user.save()


Example with Tornado Request Handler
=====================================

::

    from asyncmongoorm.collection import Collection
    from asyncmongoorm.session import Session
    from asyncmongoorm.field import StringField, ObjectIdField, BooleanField, DateTimeField

    from datetime import datetime
    import tornado.web
    from tornado import gen

    class User(Collection):

        __collection__ = "user"

        _id = ObjectIdField()
        name = StringField()
        active = BooleanField()
        created = DateTimeField()


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


Using Signals
=============

Asynmongo-ORM supports :py:mod:~`asyncmongoorm.signals` for pre_save, post_save, 
pre_remove, post_remove, pre_update, post_update to which receivers could bind to.

::

    from asyncmongoorm.collection import Collection
    from asyncmongoorm.session import Session
    from asyncmongoorm.field import StringField, ObjectIdField, BooleanField, DateTimeField
    from asyncmongoorm.signal import pre_save, receiver
    from bson import ObjectId

    import tornado.web
    from tornado import gen

    class User(Collection):
        __collection__ = "user"

        _id = ObjectIdField()
        name = StringField()
        active = BooleanField()
        created = DateTimeField()

    @receiver(pre_save, User)
    def set_object_id(sender, instance):
        if not instance._id:
            instance._id = ObjectId()


    class Handler(tornado.web.RequestHandler):

        @tornado.web.asynchronous
        @gen.engine
        def get(self):
            user = User()
            user.name = "User name"
            user.active = True
            user.created = datetime.now()

            yield gen.Task(user.save)
