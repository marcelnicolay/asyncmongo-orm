.. Asyncmongo ORM documentation master file, created by
   sphinx-quickstart on Fri Apr 20 18:30:31 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==========================================
Welcome to Asyncmongo ORM's documentation!
==========================================

Asyncmongo-ORM is a object-relation mapping for asyncmongo. 
`AsyncMongo <https://github.com/bitly/asyncmongo>`_ is an 
asynchronous library for accessing mongo which is built 
on the tornado ioloop.

Features
========

 * Maps a :class:`~asyncmongoorm.collection.Collection`
 * Maps :py:mod:`~asyncmongoorm.field` s of type (object_id, object, list, boolean, datetime, integer, string)
 * :class:`~asyncmongoorm.session.Session` facade to connection client
 * Support to :meth:`~asyncmongoorm.manager.Manager.find`, :meth:`~asyncmongoorm.manager.Manager.find_one`, :meth:`~asyncmongoorm.manager.Manager.count`, :meth:`~asyncmongoorm.manager.Manager.sum`, :meth:`~asyncmongoorm.manager.Manager.geo_near` and :meth:`~asyncmongoorm.manager.Manager.command`
 * Signals for pre_save, post_save, pre_remove, post_remove, pre_update, post_update


Contents:
=========

.. toctree::
   :maxdepth: 2

   installation
   tutorial
   apireference


Contributing to the project
===========================

`List of contributors <https://github.com/marcelnicolay/asyncmongo-orm/contributors>`_

Source Code
-----------

The source is available on `GitHub <https://github.com/marcelnicolay/asyncmongo-orm>`_ and contributions are welcome.

Issues
------

Please report any issues via `github issues <https://github.com/marcelnicolay/asyncmongo-orm/issues>`_


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

