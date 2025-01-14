from fastapi import FastAPI, Depends
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo import MongoClient
import sib_api_v3_sdk 
from sib_api_v3_sdk.rest import ApiException
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
from Router import delivery, customer #import delivery router 


load_dotenv()
security = HTTPBearer()

# global value variable for application
unDeletable = ['uncategorize', 'curry', 'pilaw rice', 'drinks', 'deserts']


app = FastAPI()

# register routers
app.include_router(delivery.route)
app.include_router(customer.router)


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
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = os.getenv('brevo')
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

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
    userDetails = user.find_one({'email' : usercredencial.email, 'role'  : usercredencial.role})
    # validate password
    if(userDetails):
        # decode password
        decoded = decodePasword(usercredencial.password, userDetails['password'])
        # validate password
        if decoded:
            # create and return JWT token
            token = encodeToken(usercredencial.email, usercredencial.password, usercredencial.role)
            return JSONResponse(status_code=200, content={'jwt_token' : token})
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
        if(store_code.modified_count == 1):
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

@app.post('/addcategory', tags=['category'])
async def addCategory(categoryData : Category, data  = Depends(authVerification)):
    # send error message if not authonticated
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # find dubplicate category
    duplicateCategory = category.find({'name' : categoryData.name}, {'_id' : 0, 'aded_date' : 0, 'last_modify_date' : 0, 'item_count' : 0})
    itemCount = 0
    for item in duplicateCategory:
        itemCount += 1
    print(itemCount)
    # if there, then send error message
    if itemCount >= 1:
        return JSONResponse(status_code=400, content='duplicate category')
    else:
        # insert in to database
        dataPoints = category.insert_one(categoryData.dict())
        # send success message
        if dataPoints.acknowledged  == True:
            return JSONResponse(status_code=200, content='successfull')
        else:
            return JSONResponse(status_code=500, content='something go wrong')
        

@app.patch('/editcategory', tags=['category'])
async def editCategory(id : str, categoryName : str,data  = Depends(authVerification)):
    pass
    # if not authonticate, then send error message
    if data == False or data['role'] != 'admin':
        return JSONResponse( status_code=401, content='unathorized')
    updatedData = category.find_one({'_id' : ObjectId(id)}, {'_id' : 0, 'deletable' : 1 })
    # find dubplicated category name from dategory collection
    duplicateCategory = list(category.find({'name' : categoryName.lower()}, {'_id' : 0, 'aded_date' : 0, 'last_modify_date' : 0, 'item_count' : 0}))
    # if there, then send error message
    if len(duplicateCategory) >= 1:
        return JSONResponse(status_code=400, content='cannot duplicate category')
    # check updated id is a unDeletable category
    if updatedData == None:
        return JSONResponse(status_code=404, content="selected category is unvailable")
    elif updatedData['deletable'] == False or updatedData['deletable'] in unDeletable:
        return JSONResponse(status_code=404, content="this category cannot updated")
    # check reseved category name
    elif categoryName in unDeletable:
        return JSONResponse(status_code=404, content=f"{categoryName} is an invalied category name.")
    # otherwise update usin _id field 
    updatedData = category.update_one({'_id' : ObjectId(id)}, { '$set' : {'name' : categoryName.lower()}})
    if updatedData.modified_count == 1:
        return JSONResponse(status_code=200, content='successfull')
    else:
        return JSONResponse(status_code=500, content='something go wrong. try again later')
        

@app.delete('/deletecategory/{categoryId}', tags=['category'])
async def deleteCategory(categoryId : str, data = Depends(authVerification)):
    pass
    # check authontication validation
    if data == False or data['role'] != 'admin':
        return JSONResponse( status_code=401, content='unathorized')
    # get category
    selectedCategory = category.find_one({'_id' : ObjectId(categoryId)})
    # if not available send error
    if selectedCategory == None:
        return JSONResponse(status_code=404, content="selected category is not available")
    # check selected category is unDeletable
    elif selectedCategory['deletable'] == False:
        return JSONResponse(status_code=404,content="this category cannot delete")
    # otherwise deleted and send success message
    else:
        deletedCategory = category.delete_one({'_id' : ObjectId(categoryId)})
        if deletedCategory.deleted_count == 1:
            return JSONResponse(status_code=200, content="successfull")
        else:
            return JSONResponse(status_code=500, content="something go wrong try latter")
            

@app.get('/getcategories', tags=['category'], response_model=List[Category])
async def getCategories(data = Depends(authVerification)):
    pass
    # authontication validation
    if data == False or data['role'] != 'admin':
        return JSONResponse( status_code=401, content='unathorized')
    # get all data
    allCategoryDetails = list(category.find({}))
    # send 
    if len(allCategoryDetails) == 0:
        return JSONResponse(status_code=404, content='categories not available')
    else:
        # convert objectId to string
        for item in allCategoryDetails:
            item['_id'] = str(item['_id'])

        return JSONResponse(status_code=200, content=jsonable_encoder(allCategoryDetails))
    
@app.post('/addfooditem', tags=['food'])
async def addFoodItem(foodData : FoodData, data = Depends(authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse( status_code=401, content='unathorized')
    # check dubplicate food item name and category id
    findCategory = category.find_one({'_id' : ObjectId(foodData.category_id)})
    dubplicateItem = list(food.find({'name' : foodData.name}))
    # if dubplicate name, then send error message
    if findCategory == None:
        return JSONResponse(status_code=409, content="category not found")
    elif len(dubplicateItem) >= 1:
        return JSONResponse(status_code=409, content="dubplicate food name")    
    # else create new food item
    else:
        insertData = food.insert_one(foodData.dict())
        if insertData.acknowledged == True:
            return JSONResponse(status_code=200, content='successfull')
        else:
            return JSONResponse(status_code=400, content='someting whent wrong')
            
@app.get('/getallfood', tags=['food'])
async def getAllFood(data = Depends(authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse( status_code=401, content='unathorized')
    # send all food 
    allFoodItems = list(food.find({}))
    for item in allFoodItems:
        item['_id'] = str(item['_id'])
        item['category_id'] = str(item['category_id'])

    return JSONResponse(status_code=200, content=jsonable_encoder(allFoodItems))

@app.patch('/editfood', tags=['food'])
async def editFoof(editfood : EditFood, data = Depends(authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse( status_code=401, content='unathorized')
    # check if _id is exist
    checkFoodId = food.find_one({"_id" : editfood.id})
    checkCategoryId = category.find_one({"_id" : editfood.category_id})
    if checkFoodId == None or checkCategoryId == None:
        return JSONResponse(status_code=404, content='cannot find food item or category')
    else:
        # update food item
        update_item = food.update_one({'_id' : editfood.id}, {'$set' : editfood.dict(exclude={'id'})})
        if update_item.modified_count == 1:
            return JSONResponse(status_code=200, content='successfull')
        else:
            return JSONResponse(status_code=500, content='something went wrong')


@app.delete('/deletefood/{foodId}', tags=['food'])
async def deleteFood( foodId : str, data = Depends(authVerification)):
    # check authontication 
    if data == False or data['role'] != 'admin':
        return JSONResponse( status_code=401, content='unathorized')
    # try to delete food 
    deletedFood = food.delete_one({'_id' : ObjectId(foodId)})
    # if success, then send success messege
    if deletedFood.deleted_count == 1:
        return JSONResponse(status_code=200, content='successfull')
    # else, send error message
    else:
        return JSONResponse(status_code=404, content='something go wrong')
        