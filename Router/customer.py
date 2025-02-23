from fastapi import APIRouter, Depends, Request
from Dependencies.database import get_database
from fastapi.responses import JSONResponse
# from Dependencies import model
# from datetime import datetime
# from fastapi.encoders import jsonable_encoder
from Dependencies.shop import doesShopOpen, get_current_meal_time
from datetime import datetime
from .docs.doc_customer import doc
from fastapi.encoders import jsonable_encoder
from Dependencies import model, authontication

route = APIRouter(prefix="/customer", tags=["customer"])
db = get_database()


@route.get('/', **doc['getFood'])
async def getFood():
    shopStatus = doesShopOpen()
    if shopStatus['status'] == True:
        data = db.get_foods()
        return data
    elif shopStatus['status'] == False:
        if shopStatus['type'] == 'closed':
            return JSONResponse(content=shopStatus['data'], status_code=403)
        elif shopStatus['type'] == 'shutdown':
            return JSONResponse(content=shopStatus['data'], status_code=403)


# @route.get('/cagegories')
# async def getCategories():
#     shopStatus = doesShopOpen()
#     if shopStatus['status'] == True:
#         # return all food items
#         data = db.get_categories_customer()
#         if len(data) > 0:
#             return JSONResponse(content=data, status_code=200)
#         else:
#             return JSONResponse(content={'message': 'No categories found'}, status_code=404)
#     else:
#         if shopStatus['type'] == 'closed':
#             return JSONResponse(content=shopStatus['data'], status_code=403)
#         elif shopStatus['type'] == 'shutdown':
#             return JSONResponse(content=shopStatus['data'], status_code=403)


@route.get('/riceAndCurry', **doc['riceAndCurry'])
async def getRiceAndCurry():
    # get current time
    meal_time = get_current_meal_time()
    if meal_time == False:
        return JSONResponse(status_code=400, content={"message": 'shop is closed'})
    else:
        # get availablie food form database
        data = db.riceAndCurryData(meal_time)
        if data['status'] == True:
            return JSONResponse(status_code=200, content={'curry': data['curry'], 'rice': data['rice'], 'rice&curry': data['rice&curry']})
        elif data['status'] == False:
            return JSONResponse(status_code=404, content={'message': 'rice and curry not available'})


@route.get('/category/{id}', **doc['undeletableCategory'])
async def getUndeletableCategory(id: str):
    # check category is undeletable or not
    category_data = db.check_undeletable_category(id)
    if category_data == False:
        return JSONResponse(status_code=400, content={'message': 'category is deletable'})
    else:
        # get current meal time
        mealTime = get_current_meal_time()
        if mealTime == False:
            return JSONResponse(status_code=400, content={'message': 'shop is closed'})
        else:
            # get data from database with serialize
            data = db.getFoodByCategory(id, mealTime)
            if data['availability'] == False:
                return JSONResponse(status_code=404, content={'message': 'foods not available', 'data': []})
            elif data['availability'] == True:
                return JSONResponse(status_code=200, content={'message': 'succssfull', 'data': data['data']})
            # return data


@route.post('/auth/mobile', **doc['mobile'])
async def checkCustomer(customer: model.customerData):
    """
    status code refference for successful message ( 200 ) :
        1000 : new account created
        1001 : alredy verified number
        1002 : verification code send to provide mobile number ( not verified number )
    """
    # check contact number is available in customer collection
    contact_number = db.check_contact_number(customer.mobile)
    if contact_number == False:
        # create customer account base on mobile number
        customer_account = db.create_customer_profile(
            customer, authontication.encodePassword(customer.mobile))
        if customer_account['status'] == True:
            return JSONResponse(status_code=200, content={'message': 'successful', 'status': 1000, 'customer': customer_account['customer']})
        else:
            return JSONResponse(status_code=500, content={"message": 'something went wrong - server'})
    else:
        # check number is verified or not
        if contact_number['verified'] == True:
            return JSONResponse(status_code=200, content={'message': 'successful', 'status': 1001})
        elif contact_number['verified'] == False:
            # send sequrity code
            sequrity_code = db.create_security_code(customer.mobile)
            if sequrity_code == True:
                return JSONResponse(status_code=200, content={'message': 'successful', 'status': 1002})
            elif sequrity_code == False:
                return JSONResponse(status_code=500, content={"message": 'something go wrong - server'})


@route.get('/auth/customerKey/{customer_key}', **doc['customerKey'])
async def verifyCustomerByKey(customer_key: str):
    """
    status code refference for successful message ( 200 ) :
        1000 : unverified customer
        1001 : alredy verified customer
    """
    # find customer by user_key
    data = db.find_customer_by_key(customer_key)
    if data['status'] == False:
        return JSONResponse(status_code=404, content={'message': 'customer not found'})
    elif data['status'] == True:
        if data['data']['verified'] == False:
            security_key = db.create_security_code_by_user_key(
                customer_key, data['data']['mobile'])
            if security_key == True:
                return JSONResponse(status_code=200, content={'message': 'successful', 'status': 1000, 'mobile_number': f'{data['data']['mobile'][:3]}****{data['data']['mobile'][7:]}'})
            else:
                return JSONResponse(status_code=200, content={'message': 'something went wrong - server'})
        elif data['data']['verified'] == True:
            return JSONResponse(status_code=200, content={'message': 'successfull', 'status': 1001})


@route.post('/auth/verification', **doc['verification'])
async def verifyCustomer(customer_verify: model.CustomerVerification):
    # check the secreate code
    data = db.check_secreate_code(customer_verify)
    if data == True:
        return JSONResponse(status_code=200, content={'message': 'successful'})
    else:
        return JSONResponse(status_code=406, content={'message': 'credencials are not matched'})
