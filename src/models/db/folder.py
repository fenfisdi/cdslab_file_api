from mongoengine import (
    BooleanField,
    EnumField,
    FileField,
    ReferenceField,
    StringField,
    UUIDField
)

from src.models.general import TypeFile
from .base import BaseDocument
from .user import User


class SimulationFolder(BaseDocument):
    simulation_uuid = UUIDField(unique=True, binary=False)
    is_deleted = BooleanField(default=False)
    user_id = ReferenceField(User, dbref=True)


class FileSimulation(BaseDocument):
    uuid = UUIDField(unique=True)
    name = StringField()
    ext = StringField(null=True)
    type = EnumField(TypeFile)
    json_image = StringField()
    simulation_folder_id = ReferenceField(SimulationFolder, dbref=True)
    file = FileField()
    region = StringField(null=True)
    variable = StringField(null=True)