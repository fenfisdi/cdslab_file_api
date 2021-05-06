from mongoengine import UUIDField, ReferenceField, StringField, BooleanField

from .base import BaseDocument
from .user import User


class SimulationFolder(BaseDocument):
    uuid = UUIDField(unique=True)
    simulation_id = UUIDField(unique=True)
    path = StringField(required=True)
    is_deleted = BooleanField()
    user_id = ReferenceField(User, dbref=True)
