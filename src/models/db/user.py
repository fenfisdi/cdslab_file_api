from mongoengine import BooleanField, StringField

from .base import BaseDocument


class User(BaseDocument):
    name = StringField()
    email = StringField(unique=True, required=True)
    is_enabled = BooleanField(default=False)
