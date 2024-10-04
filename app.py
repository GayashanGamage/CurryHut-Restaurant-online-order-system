from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo import MongoClient
import sib_api_v3_sdk 
from sib_api_v3_sdk.rest import ApiException
import os 
from dotenv import load_dotenv
from pydantic import BaseModel
from datetime import datetime
from jose import jwt
from passlib.hash import pbkdf2_sha256
from random import randint
from datetime import datetime
from fastapi.encoders import jsonable_encoder

load_dotenv()
app = FastAPI()

# CORS midleware
origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost",
    "http://localhost:5173",
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

# brevo mail server
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = os.getenv('brevo')
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

# dependent functions
# create JWT joken
def encodeToken(email, password):
    token = jwt.encode({'email' : email, 'password' : password}, os.getenv('token'), algorithm='HS256')
    return token

# decode JWT token
def decodeToken(token):
    data = jwt.decode(token, os.getenv('token'), algorithms=['HS-256'])
    return data

# encode password 
def encodePassword(palinPassword):
    encriptPassword = pbkdf2_sha256.hash(palinPassword)    
    return encriptPassword

# decode password
def decodePasword(palinPassword, encriptPassword):
    decriptedPassword = pbkdf2_sha256.verify(palinPassword, encriptPassword)
    return decriptedPassword


class userCredencials(BaseModel):
    email : str
    password : str

class UserDetails(userCredencials):
    first_name : str
    last_name : str
    type : str
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


@app.post('/createAdminAccount')
async def createAdminUserAccount(userdetials : UserDetails ):
    # find existing data from database
    adminUser = user.find_one({'email' : userdetials.email, 'type' : userdetials.type})
    print(adminUser)
    if adminUser:
        return JSONResponse(status_code=406 , content="email registered" )

    # asign encript password to plain-password
    userdetials.password = encodePassword(userdetials.password)
    # store data
    store = user.insert_one(userdetials.dict())
    if(store.acknowledged == True):

        # send mail
        subject = "Admin account created"
        sender = {"name":"Administration account creation","email":"gayashan.randimagamage@gmail.com"}
        to = [{"email":userdetials.email,"name":userdetials.first_name + userdetials.last_name}]
        headers = {"Some-Custom-Name":"unique-id-1234"}
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, sender=sender, subject=subject, template_id=6)

        api_response = api_instance.send_transac_email(send_smtp_email)
        if len(api_response.message_id) == 0:
            return JSONResponse(status_code=500, content='email cannot send')

        return JSONResponse(status_code=200, content="successfull")
    else:
        return JSONResponse(status_code=422 , content="something go wrong")
    
@app.post('/login')
async def login(usercredencial : userCredencials):
    # get user data from database
    userDetails = user.find_one({'email' : usercredencial.email})
    # validate password
    if(userDetails):
        # decode password
        decoded = decodePasword(usercredencial.password, userDetails['password'])
        # validate password
        if decoded:
            # create and return JWT token
            token = encodeToken(usercredencial.email, usercredencial.password)
            return JSONResponse(status_code=200, content={'token' : token})
        # password invalied error
        else:
            return JSONResponse(status_code=406, content='password incorect')
    # email not found error
    else:
        return JSONResponse(status_code=404, content='email not found')


@app.get('/secreatecode')
async def createSereateCode(email : str):
    # find email
    userDetails = user.find_one({'email' : email})
    # if exist create screate code and send via email, then return 'successfull' message
    if userDetails:
        # generate secreate code 
        code = randint(1000, 9999)
        # store secreate code in database
        store_code = user.update_one({'email' : email}, {'$set' : {'secreate_code' : code, 'send_time' : datetime.now(), 'password_change' : True}})
        # check whethere code is store or not
        if(store_code.modified_count <= 1):
            # send email
            subject = "Send seacreate code"
            sender = {"name":"secrete code","email":"gayashan.randimagamage@gmail.com"}
            to = [{"email":email,"name": userDetails['first_name']}]
            headers = {"Some-Custom-Name":"unique-id-1234"}
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, sender=sender, subject=subject, template_id=7, params={"code" : code})

            api_response = api_instance.send_transac_email(send_smtp_email)
            print(api_response)
            if len(api_response.message_id) == 0:
                return JSONResponse(status_code=500, content='email cannot send')

            return JSONResponse(status_code=200, content="successfull")
        else:
            return JSONResponse(status_code=404, content='something went wrong')
    # else not return 'email not found' message
    else:
        return JSONResponse(status_code=401, content='email not found')

@app.post('/codeverification')
async def codeverification(code : Code):
    # get user details
    UserDetails = user.find_one({'email' : code.email})
    # compaire secrete code and changerbility
    if(UserDetails['password_change'] and UserDetails['secreate_code'] == code.code):
        # reset secrete code and password_change
        user.update_one({'email' : code.email}, {'$set' : {'secreate_code' : None, 'send_time' : None}})
        # send successfull message
        return JSONResponse(status_code=200, content='successfull')
    # send error message
    else:
        return JSONResponse(status_code=404, content='incorect secrete code')
        

@app.post('/resetpassword')
async def resetpassword(password : Password):
    # get user detials 
    UserDetails = user.find_one({'email' : password.email})
    # check 'password_change' == true ?
    if(UserDetails['password_change'] == True):
        # encode password
        encode = encodePassword(password.password)
        # update password
        update = user.update_one({'email' : password.email}, {'$set' : {'password' : encode, 'password_change' : False}})
        # check update
        if(update.modified_count == 1):
            # send 'successfull' message
            return JSONResponse(status_code=200, content='successfull')
        else:
            return JSONResponse(status_code=404, content='something went wrong')
    # send unseccessfull message
    else:
        return JSONResponse(status_code=400, content='something went wrong')
    
# setting page endpoints --------------
# change meal time of the shop
@app.patch('/changeMealTime', tags=['setting page'])
async def changeMealTime(mealTime : str, h : int, m : int):
    # check authontication
        # if authontication fail then return error message
    # check mealtime 
    if mealTime == 'breakfast' or mealTime =='lunch' or mealTime == 'dinner': 
        # get related data from database
        timeData = shop.find_one({})
        # time comparison and send error message
        if(mealTime == 'breakfast'):
            comparison = datetime(year=1970, month=1, day=1, hour=4, minute=00).time() < datetime(year=1970, month=1, day=1, hour=h, minute=m).time() < timeData['lunch'].time()
            if comparison == False:
                return JSONResponse(status_code=400, content=f'enter time between 4:00 am and {timeData["lunch"].time()}')
        elif(mealTime == 'lunch'):
            comparison = timeData['breakfast'].time() < datetime(year=1970, month=1, day=1, hour=h, minute=m).time() < timeData['dinner'].time()
            if comparison == False:
                return JSONResponse(status_code=400, content=f'enter time between {timeData["breakfast"].time()}am and {timeData["dinner"].time()}pm')
        elif(mealTime == 'dinner'):  
            comparison = timeData['lunch'].time() < datetime(year=1970, month=1, day=1, hour=h, minute=m).time() < datetime(year=1970, month=1, day=1, hour=0, minute=00).time()
            if comparison == False:
                return JSONResponse(status_code=400, content=f'enter time between {timeData["lunch"].time()}pm and 00:00')
        
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
async def changeShopTime(shopTime : str, h : int, m : int):
    # check authontication
        # if authontication fail then return error message
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
async def operationHold():
    pass
    # get existing status of the shop from database
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
async def shopDetials():
    # check authontication
        # if authontication fail, then return error message
    shopData = shop.find_one({},{'_id' : 0})
    a = jsonable_encoder(shopData)
    return JSONResponse(status_code=200, content=a)