from fastapi import APIRouter, Depends
from Dependencies.database import get_database
from fastapi.responses import JSONResponse
from Dependencies import model
from datetime import datetime
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/customer" , tags=["customer"])
db = get_database()


@router.get('/')
async def getFood(id : str):
    data = db.get_shop_details(id)
    currentTime = datetime.now().time()
    print(f"open-time {data['open_time']} close-time {data['close_time']} current-time {currentTime}")
    
    if data['open_time'].time() < currentTime < data['close_time'].time():
        return JSONResponse(status_code=200, content={'message' : 'success'})
    
    elif currentTime < data['open_time'].time() or data['close_time'].time() < currentTime:
        shopTime = model.shop_time(open_time = datetime.fromisoformat(str(data['open_time'])), close_time = datetime.fromisoformat(str(data['close_time'])))
        return JSONResponse(status_code = 403, content = jsonable_encoder(shopTime))
