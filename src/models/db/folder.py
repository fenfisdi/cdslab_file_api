from mongoengine import (
    UUIDField,
    ReferenceField,
    BooleanField
)

from .base import BaseDocument
from .user import User


class UserFolder(BaseDocument):
    uuid = UUIDField(unique=True)
    is_deleted = BooleanField(default=False)
    user_id = ReferenceField(User, dbref=True, unique=True)


class SimulationFolder(BaseDocument):
    simulation_uuid = UUIDField(unique=True)
    is_deleted = BooleanField(default=False)
    user_folder_id = ReferenceField(UserFolder, dbref=True)
    user_id = ReferenceField(User, dbref=True)
