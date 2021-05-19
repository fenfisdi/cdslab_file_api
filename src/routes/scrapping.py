from typing import List
from fastapi import APIRouter
from hashlib import sha256
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK

from src.utils.encoder import BsonObject
from src.utils.messages import ScrappingMessage
from src.utils.response import UJSONResponse
from src.interfaces.scrapping import scrappingInterface

scrapping_routes = APIRouter(tags=['scrapping'])

@scrapping_routes.get('/scrapping/dates')
def dates_valid():
    pass


@scrapping_routes.get('/scrapping/regions')
def region_name(hash: str = None):
    
    if hash is None:
        regions = scrappingInterface.find_all()
    else:
        regions = scrappingInterface.find_one(hash)

    return UJSONResponse(
        ScrappingMessage.found,
        HTTP_200_OK,
        BsonObject.dict(regions)
    )
    

@scrapping_routes.get('/scrapping/hash')
def has_region(region: str):
    hash = sha256(f"{region}".encode('utf-8')).hexdigest()
    
    return UJSONResponse(
        ScrappingMessage.create,
        HTTP_200_OK,
        hash
    )

