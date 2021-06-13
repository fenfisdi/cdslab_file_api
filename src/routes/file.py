from io import BytesIO
from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import StreamingResponse
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.interfaces import FolderInterface, SimulationFileInterface
from src.models.general import TypeFile
from src.use_cases import FileUseCase, SaveFileUseCase, SecurityUseCase
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
    """src/models/db/__init__.py

    :param uuid:
    :param file_type:
    :param file:
    :param user:
    """
    if not FileUseCase.validate_file(file.filename):
        return UJSONResponse(FileMessage.invalid, HTTP_400_BAD_REQUEST)

    folder = FolderInterface.find_one_by_simulation(uuid, user)
    if not folder:
        return UJSONResponse(FolderMessage.not_found, HTTP_400_BAD_REQUEST)

    response, _ = SaveFileUseCase.handle(folder, file_type, file)
    return response


@file_routes.get('/simulation/{simulation_uuid}/file')
def list_files(simulation_uuid: UUID, user=Depends(SecurityUseCase.validate)):
    """

    :param simulation_uuid:
    :param user:
    """
    simulation = FolderInterface.find_one_by_simulation(
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
    simulation_folder = FolderInterface.find_one_by_simulation(
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
    simulation_folder = FolderInterface.find_one_by_simulation(
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
