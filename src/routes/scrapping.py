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
from src.models.db.scrapping import INSData

scrapping_routes = APIRouter(tags=['scrapping'])

@scrapping_routes.get('/scrapping/dates')
def dates_valid(file_id: str):
    """
    Find valid dates for a region

    :param file_id: file id
    """
    data = ScrappingInterface.find_one_data(file_id)

    if not data:
        return UJSONResponse(
            ScrappingMessage.not_found,
            HTTP_404_NOT_FOUND
        )

    dates_region = {
        'init_date': data.init_date,
        'final_date': data.final_date,
    }
    
    return UJSONResponse(
        ScrappingMessage.found,
        HTTP_200_OK,
        dates_region
    )


@scrapping_routes.get('/scrapping/regions')
def region_name(hash: str = None):
    """
    Search regions

    :param hash: region hash
    """
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
    """
    create the hash for a region

    :param region: region name
    """
    hash_region = sha256(f"{region}".encode('utf-8')).hexdigest()
    
    return UJSONResponse(
        ScrappingMessage.create,
        HTTP_200_OK,
        hash_region
    )

@scrapping_routes.post('/scrapping/Data')
def insert_ins_data(data: Data):
    """
    Save file data 

    :param data: file data
    """
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
    """
    get the data from a file

    param file_id: file id
    """
    data_found = ScrappingInterface.find_one_data(file_id)

    if not data_found:
        return UJSONResponse(ScrappingMessage.not_exist,HTTP_400_BAD_REQUEST)

    return UJSONResponse(
        ScrappingMessage.exist,
        HTTP_200_OK, 
        BsonObject.dict(data_found))
