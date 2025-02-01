from fastapi import FastAPI, Depends
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo import MongoClient
# import sib_api_v3_sdk 
# from sib_api_v3_sdk.rest import ApiException
import os 
from dotenv import load_dotenv
from pydantic import BaseModel, Field, validator, root_validator, field_validator
from datetime import datetime
from jose import jwt, JWTError
from passlib.hash import pbkdf2_sha256
from random import randint
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from bson.objectid import ObjectId
from typing import List, Optional
# import routers
from Router import delivery, customer, category, food, adminAuth, seting


load_dotenv()
security = HTTPBearer()

# global value variable for application
unDeletable = ['uncategorize', 'curry', 'pilaw rice', 'drinks', 'deserts']


app = FastAPI()

# register routers
app.include_router(delivery.route)
app.include_router(customer.router)
app.include_router(category.route)
app.include_router(food.route)
app.include_router(adminAuth.route)
app.include_router(seting.route) 


# CORS midleware
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost",
    "https://localhost",
    "http://localhost",
    "https://admin.gamage.me",
    "curryhut-admin.netlify.app",
    "https://curryhut-admin.netlify.app",
    "https://curryhut.gamage.me",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mongodb database
client = MongoClient(os.getenv('mongodb'))
db = client['curryhut']
user = db['User']
shop = db['Shop']
category = db['Category']
food = db['Food']

# brevo mail server
# configuration = sib_api_v3_sdk.Configuration()
# configuration.api_key['api-key'] = os.getenv('brevo')
# api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

# dependent functions
# create JWT joken
def encodeToken(email, password, role):
    token = jwt.encode({'email' : email, 'password' : password, 'role' : role}, os.getenv('jwt_token'), algorithm='HS256')
    return token

# decode JWT token
def decodeToken(token):
    try:
        data = jwt.decode(token, os.getenv('jwt_token'), algorithms=['HS256'])
        return data
    except JWTError:
        return False


# encode password 
def encodePassword(palinPassword):
    encriptPassword = pbkdf2_sha256.hash(palinPassword)    
    return encriptPassword

# decode password
def decodePasword(palinPassword, encriptPassword):
    decriptedPassword = pbkdf2_sha256.verify(palinPassword, encriptPassword)
    return decriptedPassword

# deal with barer token
def authVerification(details : Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    return decodeToken(details.credentials)

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
