from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from src.interfaces import FolderInterface
from src.use_cases import SecurityUseCase
from src.utils.messages import FolderMessage
from src.utils.response import UJSONResponse

folder_routes = APIRouter(tags=['Folder'])


@folder_routes.post('/folder/{simulation_uuid}')
def create_user_folder(
    simulation_uuid: UUID,
    user=Depends(SecurityUseCase.validate)
):
    simulation_found = FolderInterface.find_one_simulation(
        simulation_uuid,
        user
    )
    if simulation_found:
        return UJSONResponse(FolderMessage.exist, HTTP_400_BAD_REQUEST)

    # TODO: Create Folder Use Case

    return UJSONResponse(FolderMessage.created, HTTP_201_CREATED)
