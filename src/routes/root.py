from uuid import UUID

from fastapi import APIRouter
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from src.interfaces import (
    RootSimulationFileInterface,
    RootSimulationFolderInterface
)
from src.utils.messages import FileMessage, FolderMessage
from src.utils.response import UJSONResponse

root_routes = APIRouter(prefix='/root', tags=['root'], include_in_schema=False)


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
