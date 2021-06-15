import pandas as pd

from io import BytesIO
from datetime import date
from hashlib import sha256

from starlette.status import (
    HTTP_201_CREATED, 
    HTTP_400_BAD_REQUEST
)

from .identifier import IdentifierUseCase
from src.interfaces.scrapping import ScrappingInterface
from src.models.general import TypeFile
from src.models.db import SimulationFolder, SimulationINS
from src.utils.response import UJSONResponse
from src.utils.encoder import BsonObject
from src.utils.messages import FileMessage

class ScrappingUseCase:

    @classmethod
    def read_csv(cls, csv: str, init_date: date, final_date: date):

        file_csv = BytesIO(csv.encode())
        df = pd.read_csv(file_csv)

        filter = df[
            (df["date"] >= str(init_date)) & (df["date"] <= str(final_date))
        ]

        return filter.head(5).to_json()
  
    @classmethod
    def save_simulation(
        cls,
        folder: SimulationFolder,
        init_date: date,
        final_date: date,
        region_name: str,
        variable: str
    ):
        try:
            file_id = sha256(f"{region_name}".encode('utf-8')).hexdigest()
            data = ScrappingInterface.find_one_data(file_id)
            
            df = pd.read_csv( BytesIO(data.file.encode()))
            final_file = df[
                (df["date"] >= str(init_date)) & (df["date"] <= str(final_date))
            ]

            simulation_file = SimulationINS(
                uuid=IdentifierUseCase.create_identifier(),
                name=f"{file_id}.csv",
                ext="csv",
                file=(
                    BytesIO(final_file.to_csv(index=False).encode())
                ),
                type=TypeFile.COMPUTED,
                json_image="",
                simulation_folder_id=folder,
                region=region_name,
                variable=variable
            )

            simulation_file.save()

            return UJSONResponse(
                FileMessage.saved,
                HTTP_201_CREATED,
                BsonObject.dict(simulation_file)
            )
        except Exception as error:
            return UJSONResponse(
                str(error), 
                HTTP_400_BAD_REQUEST
            )
        