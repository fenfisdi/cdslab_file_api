from datetime import date
from uuid import UUID
from pydantic import BaseModel, Field


class Data(BaseModel):
    file_id: str = Field(...)
    file: str = Field(...)
    region: str = Field(...)
    init_date: date = Field(...)
    final_date: date = Field(...)


class SimulationIns(BaseModel):
    uuid: UUID = Field(...)
    init_date: date = Field(...)
    final_date: date = Field(...)
    region_name: str = Field(...)
    variable: str = Field(...)
