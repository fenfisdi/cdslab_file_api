from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class NewFolder(BaseModel):
    email: EmailStr = Field(...)
    simulation_uuid: UUID = Field(...)
