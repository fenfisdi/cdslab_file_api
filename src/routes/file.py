from io import BytesIO
from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import StreamingResponse
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.interfaces import SimulationFileInterface, SimulationFolderInterface
from src.models.db import FileSimulation
from src.models.general import TypeFile
from src.use_cases import FileUseCase, IdentifierUseCase, SecurityUseCase
from src.utils.encoder import BsonObject
from src.utils.messages import FileMessage, FolderMessage
from src.utils.response import UJSONResponse

file_routes = APIRouter(tags=['File'])


@file_routes.post('/simulation/{uuid}/file')
def upload_file(
    uuid: UUID,
    file_type: TypeFile = TypeFile.UPLOAD,
    file: UploadFile = File(...),
    user=Depends(SecurityUseCase.validate)
    ):
    """

    :param uuid:
    :param file_type:
    :param file:
    :param user:
    """
    if not FileUseCase.validate_file(file.filename):
        return UJSONResponse(FileMessage.invalid, HTTP_400_BAD_REQUEST)
    folder = SimulationFolderInterface.find_one_by_simulation(uuid, user)
    if not folder:
        return UJSONResponse(FolderMessage.not_found, HTTP_400_BAD_REQUEST)

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
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)

    return UJSONResponse(
        FileMessage.saved,
        HTTP_201_CREATED,
        BsonObject.dict(simulation_file)
    )


@file_routes.get('/simulation/{simulation_uuid}/file')
def list_files(simulation_uuid: UUID, user=Depends(SecurityUseCase.validate)):
    """

    :param simulation_uuid:
    :param user:
    """
    simulation = SimulationFolderInterface.find_one_by_simulation(
        simulation_uuid,
        user
    )
    if not simulation:
        return UJSONResponse(FolderMessage.not_found, HTTP_400_BAD_REQUEST)

    files = SimulationFileInterface.find_all(simulation)

    return UJSONResponse(FileMessage.found, HTTP_200_OK, BsonObject.dict(files))


@file_routes.get('/simulation/{simulation_uuid}/file/{file_uuid}')
def find_file(
    simulation_uuid: UUID,
    file_uuid: UUID,
    user=Depends(SecurityUseCase.validate)
    ):
    simulation_folder = SimulationFolderInterface.find_one_by_simulation(
        simulation_uuid,
        user
    )

    if not simulation_folder:
        return UJSONResponse(FolderMessage.not_found, HTTP_400_BAD_REQUEST)

    file_simulation = SimulationFileInterface.find_one(
        simulation_folder,
        file_uuid
    )

    if not file_simulation:
        return UJSONResponse(FileMessage.not_found, HTTP_404_NOT_FOUND)

    file = BytesIO(file_simulation.file.read())
    headers = {}

    return StreamingResponse(
        file,
        media_type='text/plain',
        headers=headers
    )


@file_routes.delete('/simulation/{simulation_uuid}/file/{file_uuid}')
def delete_file(
    simulation_uuid: UUID,
    file_uuid: UUID,
    user=Depends(SecurityUseCase.validate)
    ):
    simulation_folder = SimulationFolderInterface.find_one_by_simulation(
        simulation_uuid,
        user
    )

    if not simulation_folder:
        return UJSONResponse(FolderMessage.not_found, HTTP_400_BAD_REQUEST)

    file_simulation = SimulationFileInterface.find_one(
        simulation_folder,
        file_uuid
    )

    try:
        file_simulation.delete()
    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)

    return UJSONResponse(FileMessage.deleted, HTTP_200_OK)
