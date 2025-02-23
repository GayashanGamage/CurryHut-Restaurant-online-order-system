from pydantic import BaseModel, field_validator, Field, root_validator, validator
from datetime import datetime
from bson.objectid import ObjectId
from typing import Optional, List
from random import randint
from typing import Optional
from datetime import datetime

unDeletable = ['uncategorize', 'curry', 'pilaw rice', 'drinks', 'deserts']


class get_delivery(BaseModel):
    id: str
    place: str
    status: bool
    cost: int


class Delivery(BaseModel):
    created_at: Optional[datetime] = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=datetime.now())
    place: str
    status: Optional[bool] = Field(default=True)
    cost: int

    @field_validator('place')
    def lowercase_name(cls, place):
        return place.lower()


class get_delivery_locations(BaseModel):
    id: str
    place: str
    cost: int
    status: bool


class delivery_update(BaseModel):
    id: str = Field(..., alias="_id")
    place: str
    cost: int
    updated_at: Optional[datetime] = Field(default=datetime.now())

    @field_validator("id")
    def validate_id(cls, value):
        return ObjectId(value)

    @validator('place', pre=True)
    def lowercase_name(cls, place):
        return place.lower()


class delivery_status(BaseModel):
    id: str = Field(..., alias="_id")
    status: bool
    updated_at: Optional[datetime] = Field(default=datetime.now())

    @field_validator("id")
    def validate_id(cls, value):
        return ObjectId(value)


class shop_time(BaseModel):
    open_time: datetime
    close_time: datetime
    shutdown: bool


class shop_details(BaseModel):
    open_time: datetime
    close_time: datetime
    breakfast: datetime
    lunch: datetime
    dinner: datetime
    menu: bool
    shutdown: bool


class get_categories_customer(BaseModel):
    id: str
    name: str
    deletable: bool


class get_price(BaseModel):
    price: int
    name: str
    portion: int


class get_foods (BaseModel):
    id: str
    name: str
    category_id: str
    description: str
    availability: bool
    price: List[get_price]


class Category(BaseModel):
    name: str
    aded_date: Optional[datetime] = Field(default=datetime.now())
    last_modify_date: Optional[datetime] = Field(default=datetime.now())
    item_count: int = Field(default=0)
    deletable: bool = Field(default=True)

    @validator('name', pre=True)
    def lowercase_name(cls, name):
        return name.lower()

    @root_validator(pre=True)
    def set_undeletable(cls, value):
        name = value.get('name')

        if name in unDeletable:
            value['deletable'] = False

        return value


class getCategories(Category):
    id: str

# food section


class FoodDataPrice(BaseModel):
    name: str
    price: int
    portion: int


class FoodData(BaseModel):
    category_id: str
    name: str
    description: str
    price: list[FoodDataPrice]
    added_data: datetime = Field(default=datetime.now())
    modified_data: datetime = Field(default=datetime.now())
    breakfast: Optional[bool] = Field(default=False)
    lunch: Optional[bool] = Field(default=False)
    dinner: Optional[bool] = Field(default=False)
    availability: Optional[bool] = Field(default=False)

    @validator('category_id', pre=False)
    def convertCategoryId(cls, value):
        return ObjectId(value)


class getFood(BaseModel):
    id: str
    category_id: str
    name: str
    description: str
    price: list[FoodDataPrice]
    added_data: datetime
    modified_data: datetime
    breakfast: bool
    lunch: bool
    dinner: bool
    availability: bool

    @validator('id', pre=False)
    def convertToId(cls, value):
        return str(value)

    @validator('category_id', pre=False)
    def convertCategoryId(cls, value):
        return str(value)


class EditFood(BaseModel):
    id: str = Field(alias='_id')
    category_id: str
    name: str
    description: str
    price: list[FoodDataPrice]
    modified_data: Optional[datetime] = Field(default=datetime.now())

    @field_validator('id', check_fields=False)
    def convertToId(cls, value):
        return ObjectId(value)

    @field_validator('category_id', check_fields=False)
    def convertToCategoryId(cls, value):
        return ObjectId(value)


class userCredencials(BaseModel):
    email: str
    password: str
    role: str


class UserDetails(userCredencials):
    first_name: str
    last_name: str
    created: datetime = None
    send_time: None
    secreate_code: None
    password_change: bool = False


class MailVerification(BaseModel):
    email: str


class Code(MailVerification):
    code: int


class Password(MailVerification):
    password: str


class Rider(BaseModel):
    mobile: int
    verification: bool = Field(default=False)
    secreate_code: Optional[int] = 0
    first_name: str
    last_name: str
    nic_number: str
    driving_licens_number: str
    vehicle_number: str
    log: bool = Field(default=False)
    order_count: Optional[int] = 0
    available: bool = Field(default=False)
    created_at: datetime = Field(default=datetime.now())

    @field_validator('secreate_code', check_fields=False)
    def generateCode(cls, value):
        value = randint(100000, 999999)
        return value


class AllRiders(Rider):
    id: str
    mobile: int
    verification: bool
    first_name: str
    last_name: str
    nic_number: str
    driving_licens_number: str
    vehicle_number: str
    log: bool
    order_count: int
    available: bool
    created_at: datetime
    # verified_at: datetime

    @field_validator('id', check_fields=False)
    def convertId(cls, value):
        return str(value)


class RiderDeleteForce(BaseModel):
    id: str = Field(..., alias="_id")
    password: str

    @field_validator('id', check_fields=False)
    def convertToId(cls, value):
        return ObjectId(value)


class RiderVerification(BaseModel):
    mobile: int
    secreate_code: Optional[int] = 0
    first_name: str

    @field_validator('secreate_code', check_fields=False)
    def generateCode(cls, value):
        value = randint(100000, 999999)
        return value


class RiderContactUpdate(BaseModel):
    new_mobile: int
    old_mobile: int
    secreate_code: int


class MenuItem(BaseModel):
    id: str
    breakfast: bool
    lunch: bool
    dinner: bool
    availability: bool

    @field_validator('id', check_fields=False)
    def convertToId(cls, value):
        return ObjectId(value)


class Menu(BaseModel):
    menu: list[MenuItem]


class curry(BaseModel):
    id: str
    name: str
    availability: bool


class plain_rice(BaseModel):
    id: str
    name: str
    availability: bool


class rice_and_curry_pack(BaseModel):
    id: str
    category_id: str
    name: str
    price: List[FoodDataPrice]
    availability: bool


class customerData(BaseModel):
    mobile: str
    # this is act like a mask for customers mobile number in the broser. - inseterd of store plain customers mobile number, this user key store
    user_key: Optional[str] = Field(default=None)
    verified: Optional[bool] = Field(default=False)
    secreate_code: Optional[int] = Field(default=None)
    created: Optional[datetime] = Field(default=datetime.now())
