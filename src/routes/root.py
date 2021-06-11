from io import BytesIO
from uuid import UUID

from fastapi import APIRouter, File, UploadFile
from starlette.responses import StreamingResponse
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.interfaces import (
    FolderInterface,
    RootSimulationFileInterface,
    RootSimulationFolderInterface,
    UserInterface
)
from src.models.db import SimulationFolder, User
from src.models.general import TypeFile
from src.models.routes import NewFolder
from src.services import UserAPI
from src.use_cases import FileUseCase, SaveFileUseCase
from src.utils.encoder import BsonObject
from src.utils.messages import FileMessage, FolderMessage
from src.utils.response import UJSONResponse

root_routes = APIRouter(prefix='/root', tags=['root'], include_in_schema=False)


@root_routes.post('/folder')
def create_simulation_folder(folder: NewFolder):
    """
    Create a folder for the simulation

    :param folder: folder information
    """
    user = UserInterface.find_one(folder.email)
    if not user:
        response, is_invalid = UserAPI.find_user(folder.email)
        if is_invalid:
            return response
        user_found = response.get('data')
        user = User(
            name=user_found.get('name'),
            email=user_found.get('email'),
            is_enabled=user_found.get('is_enabled'),
        )
        try:
            user.save()
        except Exception as error:
            return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)

    folder_found = FolderInterface.find_one_by_simulation(folder.simulation_uuid, user)
    if folder_found:
        return UJSONResponse(FolderMessage.exist, HTTP_400_BAD_REQUEST)

    new_folder = SimulationFolder(
        simulation_uuid=folder.simulation_uuid,
        user_id=user
    )
    try:
        new_folder.save()
    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)

    return UJSONResponse(
        FolderMessage.created,
        HTTP_201_CREATED,
        BsonObject.dict(new_folder)
    )


@root_routes.post('/simulation/{simulation_id}')
def delete_simulation_files(simulation_id: UUID):
    """
    Delete a simulation

    :param simulation_id: Simulation uuid
    """
    simulation_folder = RootSimulationFolderInterface.find_one_by_simulation(
        simulation_id
    )
    if not simulation_folder:
        return UJSONResponse(FolderMessage.not_found, HTTP_400_BAD_REQUEST)

    simulation_files = RootSimulationFileInterface.find_all_files(
        simulation_folder
    )
    if not simulation_files:
        return UJSONResponse(FileMessage.not_found, HTTP_400_BAD_REQUEST)

    try:
        simulation_folder.is_deleted = True
        for file in simulation_files:
            file.file.delete()
            file.delete()
        simulation_folder.save()

    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)

    return UJSONResponse(FileMessage.deleted, HTTP_200_OK)


@root_routes.post('/simulation/{simulation_uuid}/file')
def upload_simulation_file(
        simulation_uuid: UUID,
        file_type: TypeFile = TypeFile.UPLOAD,
        file: UploadFile = File(...)
):
    """
    Upload a simulation file

    :param simulation_uuid: Simulation id
    :param file_type:     
    """
    if not FileUseCase.validate_file(file.filename):
        return UJSONResponse(FileMessage.invalid, HTTP_400_BAD_REQUEST)
    folder = RootSimulationFolderInterface.find_one_by_simulation(simulation_uuid)
    if not folder:
        return UJSONResponse(FolderMessage.not_found, HTTP_400_BAD_REQUEST)

    response, _ = SaveFileUseCase.handle(folder, file_type, file)
    return response


@root_routes.get('/simulation/{uuid}/file')
def list_simulation_file(uuid: UUID):
    """
    Show all files in a folder
    
    :param uuid: folder id
    """
    folder = RootSimulationFolderInterface.find_one_by_simulation(uuid)
    if not folder:
        return UJSONResponse(FolderMessage.not_found, HTTP_404_NOT_FOUND)

    files = RootSimulationFileInterface.find_all_files(folder)
    if not folder:
        return UJSONResponse(FileMessage.not_found, HTTP_404_NOT_FOUND)

    return UJSONResponse(
        FileMessage.found,
        HTTP_200_OK,
        BsonObject.dict(files)
    )


@root_routes.get('/simulation/{simulation_uuid}/file/{uuid}')
def find_simulation_file(simulation_uuid: UUID, uuid: UUID):
    """
    Search for a simulation file

    :param simulation_uuid:simulation id
    :param uuid: file id
    """
    folder = RootSimulationFolderInterface.find_one_by_simulation(
        simulation_uuid
    )
    if not folder:
        return UJSONResponse(FolderMessage.not_found, HTTP_404_NOT_FOUND)

    file = RootSimulationFileInterface.find_one(folder, uuid)
    if not file:
        return UJSONResponse(FileMessage.not_found, HTTP_404_NOT_FOUND)

    file = BytesIO(file.file.read())
    headers = {}

    return StreamingResponse(
        file,
        media_type='text/plain',
        headers=headers
    )
