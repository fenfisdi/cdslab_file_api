from uuid import UUID

from fastapi import APIRouter, File, UploadFile
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from src.interfaces import (RootSimulationFileInterface,
                            RootSimulationFolderInterface,
                            SimulationFolderInterface, UserInterface)
from src.models.db import FileSimulation, SimulationFolder, User
from src.models.general import TypeFile
from src.models.routes import NewFolder
from src.services import UserAPI
from src.use_cases import FileUseCase, IdentifierUseCase
from src.utils.encoder import BsonObject
from src.utils.messages import FileMessage, FolderMessage
from src.utils.response import UJSONResponse

root_routes = APIRouter(prefix='/root', tags=['root'], include_in_schema=False)


@root_routes.post('/folder')
def create_simulation_folder(folder: NewFolder):
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

    folder_found = SimulationFolderInterface.find_one_by_simulation(folder.simulation_uuid, user)
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

    :param simulation_id:
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
        simulation_files.delete()
        simulation_folder.save()

    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)

    return UJSONResponse(FileMessage.deleted, HTTP_200_OK)


@root_routes.post('/simulation/{simulation_id}/file')
def upload_simulation_file(
        uuid: UUID,
        file_type: TypeFile = TypeFile.UPLOAD,
        file: UploadFile = File(...)
):
    if not FileUseCase.validate_file(file.filename):
        return UJSONResponse(FileMessage.invalid, HTTP_400_BAD_REQUEST)
    folder = RootSimulationFolderInterface.find_one_by_simulation(uuid)
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
