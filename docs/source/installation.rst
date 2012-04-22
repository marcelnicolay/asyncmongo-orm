Installation
============



Supported Installation Methods
-------------------------------

Asyncmongo-ORM supports installation using standard Python "distutils" or
"setuptools" methodologies. An overview of potential setups is as follows:

* **Plain Python Distutils** - Asyncmongo-ORM can be installed with a clean
  Python install using the services provided via `Python Distutils <http://docs.python.org/distutils/>`_,
  using the ``setup.py`` script. 
* **Standard Setuptools** - When using `setuptools <http://pypi.python.org/pypi/setuptools/>`_, 
  Asyncmongo-ORM can be installed via ``setup.py`` or ``easy_install``.
* **Distribute** - With `distribute <http://pypi.python.org/pypi/distribute/>`_, 
  Asyncmongo-ORM can be installed via ``setup.py`` or ``easy_install``.
* **pip** - `pip <http://pypi.python.org/pypi/pip/>`_ is an installer that
  rides on top of ``setuptools`` or ``distribute``, replacing the usage
  of ``easy_install``.  It is often preferred for its simpler mode of usage.

.. note:: 

   It is strongly recommended that either ``setuptools`` or ``distribute`` be installed.
   Python's built-in ``distutils`` lacks many widely used installation features.

Install via easy_install or pip
-------------------------------

When ``easy_install`` or ``pip`` is available, the distribution can be 
downloaded from Pypi and installed in one step::

    easy_install asyncmongororm 

Or with pip::

    pip install asyncmongororm

This command will download the latest version of Asyncmongo-ORM from the `Python
Cheese Shop <http://pypi.python.org/pypi/asyncmongoorm>`_ and install it to your system.

Installing using setup.py
----------------------------------

Otherwise, you can install from the distribution using the ``setup.py`` script::

    python setup.py install

Checking the Installed Asyncmongo-ORM Version
---------------------------------------------

The version of Asyncmongo-ORM installed can be checked from your
Python prompt like this:

.. sourcecode:: python

     >>> import asyncmongoorm 
     >>> asyncmongoorm.__version__ # doctest: +SKIP
     '0.3.2'


Requirements
------------

The following three python libraries are required.

  * `pymongo <http://github.com/mongodb/mongo-python-driver>`_ version 1.9+ for bson library
  * `tornado <http://github.com/facebook/tornado>`_
  * `asyncmongo <http://github.github.com/bitly/asyncmongo>`_

.. note::
   The above requirements are automatically managed when installed using
   any of the supported installation methods
