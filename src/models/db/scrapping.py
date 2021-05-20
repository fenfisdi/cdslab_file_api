from .base import BaseDocument
from mongoengine import (
        StringField, 
        DateTimeField, 
        BooleanField)

class INSData(BaseDocument):
    file_id = StringField(required=True)
    path = StringField(required=True)
    region = StringField(required=True)
    init_date = DateTimeField(required=True)
    final_date = DateTimeField(required=True)

class Region(BaseDocument):
    hash = StringField(required=True)
    name = StringField(required=True)
    active = BooleanField(default=True)