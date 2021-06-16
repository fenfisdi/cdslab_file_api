from os import environ

from mongoengine import connect

from src.utils.patterns import Singleton


class MongoEngine(metaclass=Singleton):
    def __init__(self):
        self.mongo_uri = environ.get('MONGO_URI')
        self.mongo_uri = "mongodb://cdsuser:cdspass@192.168.20.42:27017/cdslib_folder?authSource=admin"

    def get_connection(self):
        return connect(host=self.mongo_uri)
