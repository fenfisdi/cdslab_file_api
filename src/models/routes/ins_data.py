from pydantic import BaseModel, Field
from datetime import date


class Data(BaseModel):
    file_id: str = Field(...)
    file: bytes = Field(...)
    region: str = Field(...)
    init_date: date = Field(...)
    final_date: date = Field(...)