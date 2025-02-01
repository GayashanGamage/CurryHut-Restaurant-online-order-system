from pydantic import BaseModel, field_validator, Field, root_validator, validator
from datetime import datetime
from bson.objectid import ObjectId
from typing import Optional, List

unDeletable = ['uncategorize', 'curry', 'pilaw rice', 'drinks', 'deserts']

class get_delivery(BaseModel):
    id : str
    place : str
    status : bool
    cost : int


class Delivery(BaseModel):
    created_at : Optional[datetime] = Field(default=datetime.now())
    updated_at : Optional[datetime] = Field(default=datetime.now())
    place : str
    status : Optional[bool] = Field(default=True)
    cost : int

class delivery_update(BaseModel):
    id : str = Field(..., alias="_id")
    place : str
    cost : int
    updated_at : Optional[datetime] = Field(default=datetime.now())

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
    
class shop_time(BaseModel):
    open_time : datetime
    close_time : datetime
    shutdown : bool 

class get_categories_customer(BaseModel):
    id : str
    name : str
    deletable : bool


class get_price(BaseModel):
    price : int
    name : str
    portion : int

class get_foods (BaseModel):
    id : str
    name : str
    category_id : str 
    description : str 
    price : List[get_price]
    
class Category(BaseModel):
    name : str
    aded_date : datetime = Field(default = datetime.now())
    last_modify_date : datetime = Field(default = datetime.now())
    item_count : int = Field(default=0)
    deletable : bool = Field(default=True)

    @validator('name', pre=True)
    def lowercase_name(cls, name):
        return name.lower()

    @root_validator(pre=True)
    def set_undeletable(cls, value ):
        name = value.get('name')
        
        if name in unDeletable:
            value['deletable'] = False

        return value
    
# food section 
class FoodDataPrice(BaseModel):
    name : str
    price : int
    portion : int

class FoodData(BaseModel):
    category_id : str
    name : str
    description : str
    price : list[FoodDataPrice]
    added_data : datetime = Field(default=datetime.now())
    modified_data : datetime = Field(default=datetime.now())

    @validator('category_id', pre=False)
    def convertCategoryId(cls, value):
        return ObjectId(value)
    
class getFood(BaseModel):
    id : str
    category_id : str
    name : str
    description : str
    price : list[FoodDataPrice]
    added_data : datetime
    modified_data : datetime
         
    @validator('id', pre=False)
    def convertToId(cls, value):
        return str(value)
    
    @validator('category_id', pre=False)
    def convertCategoryId(cls, value):
        return str(value)

class EditFood(BaseModel):
    id : str = Field(alias='_id')
    category_id : str
    name : str
    description : str
    price : list[FoodDataPrice]
    modified_data : Optional[datetime] = Field(default=datetime.now())

    @field_validator('id', check_fields=False)
    def convertToId(cls, value):
        return ObjectId(value)

    @field_validator('category_id', check_fields=False)
    def convertToCategoryId(cls, value):
        return ObjectId(value)
    
class userCredencials(BaseModel):
    email : str
    password : str
    role : str

class UserDetails(userCredencials):
    first_name : str
    last_name : str
    created : datetime = None
    send_time : None
    secreate_code : None
    password_change : bool = False
    
class MailVerification(BaseModel):
    email : str

class Code(MailVerification):
    code : int

class Password(MailVerification):
    password : str