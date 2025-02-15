from fastapi import APIRouter, Depends
from Dependencies.database import get_database
from fastapi.responses import JSONResponse
# from Dependencies import model
# from datetime import datetime
# from fastapi.encoders import jsonable_encoder
from Dependencies.shop import doesShopOpen, get_current_meal_time
from datetime import datetime
from .docs.doc_customer import doc

route = APIRouter(prefix="/customer", tags=["customer"])
db = get_database()


@route.get('/')
async def getFood():
    shopStatus = doesShopOpen()
    if shopStatus['status'] == True:
        data = db.get_foods()
        return data
    else:
        if shopStatus['type'] == 'closed':
            return JSONResponse(content=shopStatus['data'], status_code=403)
        elif shopStatus['type'] == 'shutdown':
            return JSONResponse(content=shopStatus['data'], status_code=403)


@route.get('/cagegories')
async def getCategories():
    shopStatus = doesShopOpen()
    if shopStatus['status'] == True:
        # return all food items
        data = db.get_categories_customer()
        if len(data) > 0:
            return JSONResponse(content=data, status_code=200)
        else:
            return JSONResponse(content={'message': 'No categories found'}, status_code=404)
    else:
        if shopStatus['type'] == 'closed':
            return JSONResponse(content=shopStatus['data'], status_code=403)
        elif shopStatus['type'] == 'shutdown':
            return JSONResponse(content=shopStatus['data'], status_code=403)


@route.get('/riceAndCurry', **doc['riceAndCurry'])
async def getRiceAndCurry():
    # get current time
    meal_time = get_current_meal_time()
    print(meal_time)
    if meal_time == False:
        return JSONResponse(status_code=400, content={"message": 'shop is closed'})
    else:
        # get availablie food form database
        data = db.riceAndCurryData(meal_time)
        print(meal_time)
        if data['status'] == True:
            return JSONResponse(status_code=200, content={'curry': data['curry'], 'rice': data['rice'], 'rice&curry': data['rice&curry']})
        elif data['status'] == False:
            return JSONResponse(status_code=404, content={'message': 'rice and curry not available'})


@route.get('/category/{id}')
async def getUndeletableCategory(id: str):
    # check category is undeletable or not
    category_data = db.check_undeletable_category(id)
    if category_data == False:
        return JSONResponse(status_code=400, content={'message': 'category is deletable'})
    else:
        # get data from database with serialize
        data = db.getFoodByCategory(id)
        if data['availability'] == False:
            return JSONResponse(status_code=400, content={'message': 'foods not available', 'data': []})
        elif data['availability'] == True:
            return JSONResponse(status_code=200, content={'message': 'succssfull', 'data': data['data']})
        # return data
