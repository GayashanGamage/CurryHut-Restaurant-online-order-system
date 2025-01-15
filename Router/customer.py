from fastapi import APIRouter, Depends
from Dependencies.database import get_database
from fastapi.responses import JSONResponse
# from Dependencies import model
# from datetime import datetime
# from fastapi.encoders import jsonable_encoder
from Dependencies.shop import doesShopOpen
from datetime import datetime

router = APIRouter(prefix="/customer" , tags=["customer"])
db = get_database()


@router.get('/')
async def getFood():
    shopStatus = doesShopOpen()
    if shopStatus['status'] == True:
        data = db.get_foods()
        return data
    else:
        if shopStatus['type'] == 'closed':
            return JSONResponse(content = shopStatus['data'], status_code = 403)
        elif shopStatus['type'] == 'shutdown':
            return JSONResponse(content = shopStatus['data'], status_code = 403)
    

@router.get('/cagegories')
async def getCategories():
    shopStatus = doesShopOpen()
    if shopStatus['status'] == True:
        # return all food items
        data = db.get_categories_customer()
        if len(data) > 0:
            return JSONResponse(content = data, status_code = 200)
        else:
            return JSONResponse(content = {'message' : 'No categories found'}, status_code = 404)
    else:
        if shopStatus['type'] == 'closed':
            return JSONResponse(content = shopStatus['data'], status_code = 403)
        elif shopStatus['type'] == 'shutdown':
            return JSONResponse(content = shopStatus['data'], status_code = 403)

