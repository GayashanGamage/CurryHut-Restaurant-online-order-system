from fastapi import APIRouter, Depends
from Dependencies import database, authontication
from fastapi.responses import JSONResponse
from datetime import datetime

route = APIRouter( tags=['setting page'])
db = database.get_database()


@route.patch('/changeMealTime')
async def changeMealTime(mealTime : str, h : int, m : int, data = Depends(authontication.authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # check mealtime and update acordingly
    if mealTime == 'breakfast' or mealTime =='lunch' or mealTime == 'dinner' and 0 <= h <= 23 and 0 <= m <= 59:
        check_meal_time = db.check_meal_time(mealTime, h, m)
        if check_meal_time['status'] == True:
            return JSONResponse(status_code=200, content='successfull')
        
        # return invalied meal time ( compare with the open, close and other meal time )
        elif check_meal_time['code'] == 450:
            return JSONResponse(status_code=400, content='invalied breakfast time')
        elif check_meal_time['code'] == 451:
            return JSONResponse(status_code=400, content='invalied lunch time')
        elif check_meal_time['code'] == 452:
            return JSONResponse(status_code=400, content='invalied dinner time')
        
        # unprocessable error ( server error )
        elif check_meal_time['code'] == 500:
            return JSONResponse(status_code=500, content='something went wrong - server')
    
    # invalied meal time name
    elif mealTime != 'breakfast' or mealTime != 'lunch' or mealTime != 'dinner':
        return JSONResponse(status_code=404, content='invalied meal-name')
    
    # invalied time
    else:
        return JSONResponse(status_code=400, content='invalid time')
  
@route.get('/shopdetails')
async def shopDetials(data = Depends(authontication.authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # get data from database and return
    shopData = db.get_shopdetails()
    return JSONResponse(status_code=200, content=shopData)


@route.patch('/operationhold')
async def operationHold(data = Depends(authontication.authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unauthorized')
    # get shop details
    shopStatus = db.get_shopdetails_row()
    # check opening time and closing time
    if shopStatus['open_time'].time() < datetime.now().time() < shopStatus['close_time'].time():
        # udpate shop status accordingly    
        status_update = db.update_shop_status(shopStatus['shutdown'])
        if status_update == True and shopStatus['shutdown'] == False:
            return JSONResponse(status_code=200, content='successfuly open')
        elif status_update == True and shopStatus['shutdown'] == True:
            return JSONResponse(status_code=200, content='successfuly close')
    else:
        return JSONResponse(status_code=400, content="you cannot change status of the shop while it's close time ")
    
    

# change shop opening and close time
@route.patch('/changeShopTime')
async def changeShopTime(shopTime : str, h : int, m : int, data = Depends(authontication.authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # check shoptime variable
    if  shopTime== 'open_time' or shopTime =='close_time': 
        # get stored data from database
        shopData = db.get_shopdetails_row()
        
        # time comparison with current time
        if shopTime == 'open_time':
            comparison = shopData['close_time'].time() < datetime(year=1970, month=1, day=1, hour=h, minute=m).time()
            if comparison == True:
                return JSONResponse(status_code=400, content='you cannot set opening time lager than existing close time.')
        elif shopTime == 'close_time':
            comparison = shopData['open_time'].time() > datetime(year=1970, month=1, day=1, hour=h, minute=m).time()
            if comparison == True:
                return JSONResponse(status_code=400, content='you cannot set close time less than existing open time')
            
        # update shop time
        shopTime = db.update_shop_time(shopTime, h, m)
        if shopTime == True:
            return JSONResponse(status_code=200, content='successfull')
        else:
            return JSONResponse(status_code=500, content='something went wrong - server')
    else:
        return JSONResponse(status_code=404, content='selected shop time name is not fond')