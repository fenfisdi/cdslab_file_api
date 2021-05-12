from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from src.interfaces import SimulationFolderInterface, UserFolderInterface
from src.models.db import UserFolder, SimulationFolder
from src.use_cases import SecurityUseCase, IdentifierUseCase
from src.utils.encoder import BsonObject
from src.utils.messages import FolderMessage
from src.utils.response import UJSONResponse

folder_routes = APIRouter(tags=['Folder'])


@folder_routes.post('/folder/user')
def create_user_folder(user=Depends(SecurityUseCase.validate)):
    folder = UserFolderInterface.find_one_by_user(user)

    if folder:
        return UJSONResponse(FolderMessage.exist, HTTP_400_BAD_REQUEST)

    user_folder = UserFolder(
        uuid=IdentifierUseCase.create_identifier(),
        user_id=user
    )

    # TODO: Create Folder Use Case

    try:
        user_folder.save()
    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)

    return UJSONResponse(FolderMessage.created, HTTP_201_CREATED)


@folder_routes.post('/folder/simulation')
def create_simulation_folder(
    uuid: UUID,
    user=Depends(SecurityUseCase.validate)
):
    user_folder = UserFolderInterface.find_one_by_user(user)
    if not user_folder:
        return UJSONResponse(FolderMessage.exist, HTTP_400_BAD_REQUEST)

    simulation_found = SimulationFolderInterface.find_one_by_simulation(
        uuid,
        user
    )
    if simulation_found:
        return UJSONResponse(FolderMessage.exist, HTTP_400_BAD_REQUEST)

    simulation_folder = SimulationFolder(
        simulation_uuid=uuid,
        user_folder_id=user_folder,
        user_id=user
    )

    try:
        simulation_folder.save()
    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)

    return UJSONResponse(
        FolderMessage.created,
        HTTP_201_CREATED,
        BsonObject.dict(simulation_folder)
    )
