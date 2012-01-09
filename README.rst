Asyncmongo-ORM
======================

Asyncmongo-ORM is a object-relation mapping for asyncmongo. AsyncMongo_ is an asynchronous library for accessing mongo which is built on the tornado ioloop.

Installation
-----------------

Installing: `pip install asyncmongoorm`

Usage
--------------

    Collection:

    >>> from asyncmongoorm.collection import Collection
    >>> from asyncmongoorm.session import Session
    >>> from asyncmongoorm.field import StringField, ObjectIdField, BooleanField, DateTimeField
    >>> from datetime import datetime
    >>>
    >>> Session.create('localhost', 27017, 'asyncmongo_test') # create asyncmongo session client
    >>>
    >>> class User(Collection):
    >>>     __collection__ = "user"
    >>> 
    >>>     _id = ObjectIdField()
    >>>     name = StringField()
    >>>     active = BooleanField()
    >>>     created = DateTimeField()
    >>>

    >>> #save data

    >>> user = User()
    >>> user.name = "User name"
    >>> user.active = True
    >>> user.created = datetime.now()
    >>> user.save()
    
    >>> # update date
    >>> user.name = "New name"
    >>> user.update()

    >>> # remove data    
    >>> user.remove()

Requirements
------------
The following three python libraries are required

* pymongo_ version 1.9+ for bson library
* tornado_
* asyncmongo_

Issues
------

Please report any issues via github issues_

.. _pymongo: http://github.com/mongodb/mongo-python-driver
.. _tornado: http://github.com/facebook/tornado
.. _asyncmongo: http://github.github.com/bitly/asyncmongo
.. _issues: https://github.com/marcelnicolay/asyncmongo-orm/issues