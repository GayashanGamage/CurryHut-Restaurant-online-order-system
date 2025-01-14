from fastapi import APIRouter, Depends
from Dependencies.database import get_database
from fastapi.responses import JSONResponse
# from Dependencies import model
# from datetime import datetime
# from fastapi.encoders import jsonable_encoder
from Dependencies.shop import doesShopOpen

router = APIRouter(prefix="/customer" , tags=["customer"])
db = get_database()


@router.get('/')
async def getFood():
    shopStatus = doesShopOpen()
    if shopStatus['status'] == True:
        # return all food items
        return JSONResponse(content ={'message' : 'open'}, status_code = 200)
    else:
        if shopStatus['type'] == 'closed':
            return JSONResponse(content = shopStatus['data'], status_code = 403)
        elif shopStatus['type'] == 'shutdown':
            return JSONResponse(content = shopStatus['data'], status_code = 403)
    
