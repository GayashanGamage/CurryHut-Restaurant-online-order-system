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


    

        