from pydantic import BaseModel, field_validator, Field
from datetime import datetime
from bson.objectid import ObjectId
from typing import Optional


class get_delivery(BaseModel):
    id : str
    place : str
    status : bool
    cost : int


class Delivery(BaseModel):
    created_at : datetime
    updated_at : datetime
    place : str
    status : bool
    cost : int

class delivery_update(BaseModel):
    id : str = Field(..., alias="_id")
    place : str
    cost : int
    updated_at : datetime

    @field_validator("id")
    def validate_id(cls, value):
        return ObjectId(value)
    
class delivery_status(BaseModel):
    id : str = Field(..., alias="_id")
    status : bool
    updated_at : Optional[datetime] = Field(default=datetime.now())

    @field_validator("id")
    def validate_id(cls, value):
        return ObjectId(value)