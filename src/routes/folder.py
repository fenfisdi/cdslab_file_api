from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED

from src.use_cases import SecurityUseCase
from src.utils.response import UJSONResponse

folder_routes = APIRouter(tags=['Folder'])


@folder_routes.post('/folder/user')
def create_user_folder(user=Depends(SecurityUseCase.validate)):
    return UJSONResponse('ok', HTTP_201_CREATED, {'hola': 'mundo'})


@folder_routes.post('/folder/simulation')
def create_simulation_folder(
    uuid: UUID,
    user=Depends(SecurityUseCase.validate)
):
    return UJSONResponse('ok', HTTP_201_CREATED, {'hola': 'mundo'})
