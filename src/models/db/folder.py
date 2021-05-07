from mongoengine import UUIDField, ReferenceField, BooleanField

from .base import BaseDocument
from .user import User


class UserFolder(BaseDocument):
    uuid = UUIDField(unique=True)
    is_deleted = BooleanField(default=False)
    user_id = ReferenceField(User, dbref=True, unique=True)


class SimulationFolder(BaseDocument):
    uuid = UUIDField(unique=True)
    simulation_id = UUIDField(unique=True)
    is_deleted = BooleanField(default=False)
    user_folder = ReferenceField(UserFolder, dbref=True)
    user_id = ReferenceField(User, dbref=True)
