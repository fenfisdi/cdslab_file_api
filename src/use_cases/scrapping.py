from datetime import date
from hashlib import sha256
from io import BytesIO

import pandas as pd
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST
)

from src.interfaces.scrapping import ScrappingInterface
from src.models.db import FileSimulation, SimulationFolder
from src.models.general import TypeFile
from src.utils.encoder import BsonObject
from src.utils.messages import FileMessage
from src.utils.response import UJSONResponse
from .identifier import IdentifierUseCase


class ScrappingUseCase:

    @classmethod
    def read_csv(cls, csv: str, init_date: date, final_date: date):

        file_csv = BytesIO(csv.encode())
        df = pd.read_csv(file_csv)

        filter = df[
            (df["date"] >= str(init_date)) & (df["date"] <= str(final_date))
        ]

        return cls.create_json_df(filter.head(5))
  
    @classmethod
    def save_simulation(
        cls,
        folder: SimulationFolder,
        init_date: date,
        final_date: date,
        region_name: str,
        variable: str
      ):
        variable_representation = {
            "infected": "I",
            "recovered": "R",
            "dead": "D",
        }
        variable_label = variable_representation.get(variable)
        assert variable_label, RuntimeError('Variable must be set')

        try:
            file_id = sha256(f"{region_name}".encode('utf-8')).hexdigest()
            data = ScrappingInterface.find_one_data(file_id)
            
            df = pd.read_csv(BytesIO(data.file.encode()))
            df = df[['date', variable_label]]
            final_file = df[
                (df["date"] >= str(init_date)) & (df["date"] <= str(final_date))
            ]

            simulation_file = FileSimulation(
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
        
    @classmethod
    def create_json_df(cls, df):
        
        columns = [column for column in df.columns]
        headers = []
        body=[]

        for name in columns:
            headers.append(
                dict(
                    label=name if not "_" in name else name.replace("_"," ").capitalize(),
                    name=name
                )
            )

        for _, row in df.iterrows():
            body.append(
                {
                  name:row[name]  for name in columns
                }
            )

        return dict(
            headers=headers,
            body=body
        )
        