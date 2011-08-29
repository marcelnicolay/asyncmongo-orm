from asyncmongo import Client
from torneira import settings

import logging

__database__ = None

def get_database():
    global __database__

    if not __database__:
        logging.info("MONGODB connecting database...")

        host= settings.database_url
        port= settings.database_port
        dbname = settings.dbname

        __database__ = Client(pool_id='mydb', host=host, port=port, dbname=dbname)

    return __database__
