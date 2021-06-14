from mongoengine import (
    BooleanField, 
    DateTimeField, 
    StringField,
    BinaryField
)

from .base import BaseDocument


class INSData(BaseDocument):
    file_id = StringField(required=True)
    file = BinaryField(required=True)
    region = StringField(required=True)
    init_date = DateTimeField(required=True)
    final_date = DateTimeField(required=True)


class Region(BaseDocument):
    hash = StringField(required=True)
    name = StringField(required=True)
    active = BooleanField(default=True)
