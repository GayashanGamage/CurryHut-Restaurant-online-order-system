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
from Router import delivery, customer, category, food, adminAuth


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
        
    
# setting page endpoints --------------
# change meal time of the shop
@app.patch('/changeMealTime', tags=['setting page'])
async def changeMealTime(mealTime : str, h : int, m : int, data = Depends(authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # check mealtime 
    if mealTime == 'breakfast' or mealTime =='lunch' or mealTime == 'dinner': 
        # get related data from database
        timeData = shop.find_one({})
        # time comparison and send error message
        if(mealTime == 'breakfast'):
            comparison = datetime(year=1970, month=1, day=1, hour=4, minute=00).time() < datetime(year=1970, month=1, day=1, hour=h, minute=m).time() < timeData['lunch'].time()
            if comparison == False:
                return JSONResponse(status_code=400, content=f'enter time between 4:00 am and {timeData["lunch"].time()} -1 ')
        elif(mealTime == 'lunch'):
            comparison = timeData['breakfast'].time() < datetime(year=1970, month=1, day=1, hour=h, minute=m).time() < timeData['dinner'].time()
            if comparison == False:
                return JSONResponse(status_code=400, content=f'enter time between {timeData["breakfast"].time()}am and {timeData["dinner"].time()}pm -2')
        elif(mealTime == 'dinner'):  
            comparison = timeData['lunch'].time() < datetime(year=1970, month=1, day=1, hour=h, minute=m).time() < datetime(year=1970, month=1, day=1, hour=23, minute=59).time()
            if comparison == False:
                return JSONResponse(status_code=400, content=f'enter time between {timeData["lunch"].time()}pm and 00:00 -3')
        
        # update meal time
        shopUpdate = shop.update_one({}, {'$set' : {mealTime : datetime(year=1970, month=1, day=1, hour=h, minute=m)}})
        # check whether meal time update or not
        # if successfull then send successfull message
        if shopUpdate.modified_count == 1:
            return JSONResponse(status_code=200, content='successfull')
        #  else send server error - due to unble to update
        else:
            return JSONResponse(status_code=500, content='something went wrong')
    else:
        return JSONResponse(status_code=404, content='meal time not found')
    

# change shop opening and close time
@app.patch('/changeShopTime', tags=['setting page'])
async def changeShopTime(shopTime : str, h : int, m : int, data = Depends(authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # check shoptime variable
    if  shopTime== 'open_time' or shopTime =='close_time': 
        # get stored data from database
        shopData = shop.find_one({})
        # time comparison
        if shopTime == 'open_time':
            comparison = shopData['close_time'].time() < datetime(year=1970, month=1, day=1, hour=h, minute=m).time()
            if comparison == True:
                return JSONResponse(status_code=400, content='you cannot set opening time lager than existing close time.')
        elif shopTime == 'close_time':
            comparison = shopData['open_time'].time() > datetime(year=1970, month=1, day=1, hour=h, minute=m).time()
            if comparison == True:
                return JSONResponse(status_code=400, content='you cannot set close time less than existing open time')
            
        # update meal time
        shopUpdate = shop.update_one({}, {'$set' : {shopTime : datetime(year=1970, month=1, day=1, hour=h, minute=m)}})
        # check whether meal time update or not
        # if successfull then send successfull message
        if shopUpdate.modified_count == 1:
            return JSONResponse(status_code=200, content='successfull')
        #  else send server error - due to unble to update
        else:
            return JSONResponse(status_code=500, content='something went wrong - server')
    else:
        return JSONResponse(status_code=404, content='selected time not fond')
    
@app.patch('/operationhold', tags=['setting page'])
async def operationHold(data = Depends(authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unauthorized')
    shopStatus = shop.find_one({})
    # check opening time and closing time
    if (shopStatus['open_time'].time() < datetime.now().time() < shopStatus['close_time'].time()) == True:
        # if above is ok then swap shutdown status
        if shopStatus['shutdown'] == True:
            shop.update_one({}, {'$set' : {'shutdown' : False}})
            return JSONResponse(status_code=200, content='successfuly open')
        elif shopStatus['shutdown'] == False:
            shop.update_one({}, {'$set' : {'shutdown' : True}})
            return JSONResponse(status_code=200, content='successfuly close')
        # else show error that shop is close
    else:
        return JSONResponse(status_code=400, content="you cannot change status of the shop while it's close time ")
    

@app.get('/shopdetails', tags=['setting page'])
async def shopDetials(data = Depends(authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # get data from database and return
    shopData = shop.find_one({},{'_id' : 0})
    a = jsonable_encoder(shopData)
    data = {
        'open_time' : datetime.fromisoformat(a['open_time']).time(),
        'close_time' : datetime.fromisoformat(a['close_time']).time(),
        'breakfast' : datetime.fromisoformat(a['breakfast']).time(),
        'lunch' : datetime.fromisoformat(a['lunch']).time(),
        'dinner' : datetime.fromisoformat(a['dinner']).time(),
        'shutdown' : a['shutdown']
    }
    b = jsonable_encoder(data)
    return JSONResponse(status_code=200, content=b)

