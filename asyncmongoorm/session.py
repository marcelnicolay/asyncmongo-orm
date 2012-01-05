from asyncmongo import Client

class Session(object):
    
    _session = None
    
    def __new__(cls, collection_name=None):

        if not cls._session:
            raise(ValueError("Session is not created"))

        if collection_name:
            return getattr(cls._session, collection_name)
            
        return cls._session
        
    @classmethod
    def create(cls, host, port, dbname, **kwargs):
        if not cls._session:
            cls._session = Client(pool_id='mydb', host=host, port=port, dbname=dbname, **kwargs)
        
    @classmethod
    def destroy(cls):
        cls._session = None

