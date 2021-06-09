from os import environ

from mongoengine import connect

from src.utils.patterns import Singleton


class MongoEngine(metaclass=Singleton):
    """
    This class controls access to the database
    """
    def __init__(self):
        self.mongo_uri = environ.get('MONGO_URI')

    def get_connection(self):
        return connect(host=self.mongo_uri)
