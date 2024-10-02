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

class UserDetails(BaseModel):
    email : str
    first_name : str
    last_name : str
    password : str
    type : str
    created : datetime = None


@app.post('/createAdminAccount')
async def createAdminUserAccount(userdetials : UserDetails ):
    # find existing data from database
    adminUser = user.find_one({'email' : userdetials.email, 'type' : userdetials.type})
    print(adminUser)
    if adminUser:
        return JSONResponse(status_code=406 , content="email registered" )

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
    

        