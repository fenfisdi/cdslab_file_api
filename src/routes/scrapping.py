from fastapi import APIRouter
from hashlib import sha256
from starlette.status import (
    HTTP_201_CREATED, 
    HTTP_400_BAD_REQUEST, 
    HTTP_200_OK, 
    HTTP_404_NOT_FOUND
)

from src.utils.encoder import BsonObject
from src.utils.messages import ScrappingMessage
from src.utils.response import UJSONResponse
from src.interfaces.scrapping import ScrappingInterface
from src.models.routes.ins_data import Data
from src.models.db.scrapping import INSData, Region

scrapping_routes = APIRouter(tags=['scrapping'])

@scrapping_routes.get('/scrapping/dates')
def dates_valid(file_id: str):
    data = ScrappingInterface.find_one_data(file_id)

    if not data:
        return UJSONResponse(
            ScrappingMessage.not_found,
            HTTP_404_NOT_FOUND
        )

    dates_region = {
        'initialDate': data.init_date.strftime("%d/%m/%Y"),
        'finalDate': data.final_date.strftime("%d/%m/%Y")
    }
    
    return UJSONResponse(
        ScrappingMessage.found,
        HTTP_200_OK,
        dates_region
    )


@scrapping_routes.get('/scrapping/regions')
def region_name(hash: str = None):
    
    if hash is None:
        regions = ScrappingInterface.find_all()
    else:
        regions = ScrappingInterface.find_one(hash)

    return UJSONResponse(
        ScrappingMessage.found,
        HTTP_200_OK,
        BsonObject.dict(regions)
    )
    

@scrapping_routes.get('/scrapping/hash')
def has_region(region: str):
    hash_region = sha256(f"{region}".encode('utf-8')).hexdigest()
    
    return UJSONResponse(
        ScrappingMessage.create,
        HTTP_200_OK,
        hash_region
    )

@scrapping_routes.post('/scrapping/Data')
def insert_ins_data(data: Data):
    data_found = ScrappingInterface.find_one_data(data.file_id)

    if data_found:
        return UJSONResponse(ScrappingMessage.exist,HTTP_400_BAD_REQUEST)

    try:
        new_data = INSData(**data.dict())
        new_data.save()
    except Exception as error:
        return UJSONResponse(str(error),HTTP_400_BAD_REQUEST)
    return UJSONResponse(ScrappingMessage.insert,HTTP_201_CREATED)
    

@scrapping_routes.get('/scrapping/Data')
def get_ins_data(file_id: str):
    data_found = ScrappingInterface.find_one_data(file_id)

    if not data_found:
        return UJSONResponse(ScrappingMessage.not_exist,HTTP_400_BAD_REQUEST)

    return UJSONResponse(
        ScrappingMessage.exist,
        HTTP_200_OK, 
        BsonObject.dict(data_found))
