from asyncmongo import Client

class Session(object):
    
    _session = None
    
    def __new__(cls):
        
        if not cls._session:
            raise(ValueError("Session is not created"))
            
        return cls._session
        
    @classmethod
    def create(cls, host, port, dbname, **kwargs):

        cls._session = Client(pool_id='mydb', host=host, port=port, dbname=dbname, **kwargs)
    
    @classmethod
    def destroy(cls):
        
        cls._session = None