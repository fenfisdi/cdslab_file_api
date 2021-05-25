from typing import Optional

from fastapi import UploadFile
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from src.models.db import FileSimulation, SimulationFolder
from src.models.general import TypeFile
from src.utils.encoder import BsonObject
from src.utils.messages import FileMessage
from src.utils.response import UJSONResponse
from .identifier import IdentifierUseCase


class FileUseCase:

    @classmethod
    def validate_file(cls, filename: str) -> bool:
        allowed_files = {'csv', 'parquet', 'pickle', 'feather', 'png', 'jpeg'}

        extension_file = cls.get_file_extension(filename)

        if extension_file in allowed_files:
            return True
        return False

    @classmethod
    def get_file_extension(cls, filename: str) -> Optional[str]:
        split_filename = filename.split('.')
        index_name = -2 if len(split_filename) > 1 else 0
        if split_filename[index_name] == split_filename[-1]:
            return None
        return split_filename[-1]


class SaveFileUseCase:

    @classmethod
    def handle(
        cls,
        folder: SimulationFolder,
        file_type: TypeFile,
        file: UploadFile
    ) -> (UJSONResponse, bool):
        simulation_file = FileSimulation(
            uuid=IdentifierUseCase.create_identifier(),
            name=file.filename,
            ext=FileUseCase.get_file_extension(file.filename),
            file=file.file.read(),
            type=file_type,
            simulation_folder_id=folder,
        )
        try:
            simulation_file.save()
        except Exception as error:
            return UJSONResponse(str(error), HTTP_400_BAD_REQUEST), False

        return UJSONResponse(
            FileMessage.saved,
            HTTP_201_CREATED,
            BsonObject.dict(simulation_file)
        ), True
