from fastapi import APIRouter, Depends, Query, Query
from Dependencies import database, authontication
from fastapi.responses import JSONResponse
from datetime import datetime
from .docs.doc_setting import doc
import pytz

route = APIRouter(tags=['setting page'])
db = database.get_database()


@route.patch('/changeMealTime', **doc['changeMealTime'])
async def changeMealTime(mealTime: str = Query(description='meal time - breakfast, lunch, dinner'),
                         h: int = Query(description='hours',
                                        gt=0, lt=24),
                         m: int = Query(description='minuts',
                                        gt=0, lt=59),
                         data=Depends(authontication.authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # check mealtime and update acordingly
    if mealTime == 'breakfast' or mealTime == 'lunch' or mealTime == 'dinner' and 0 <= h <= 23 and 0 <= m <= 59:
        check_meal_time = db.check_meal_time(mealTime, h, m)
        if check_meal_time['status'] == True:
            return JSONResponse(status_code=200, content={'message': 'successful'})

        # return invalied meal time ( compare with the open, close and other meal time )
        elif check_meal_time['code'] == 450:
            return JSONResponse(status_code=400, content={'message': 'invalied breakfast time'})
        elif check_meal_time['code'] == 451:
            return JSONResponse(status_code=400, content={'message': 'invalied lunch time'})
        elif check_meal_time['code'] == 452:
            return JSONResponse(status_code=400, content={'message': 'invalied dinner time'})

        # unprocessable error ( server error )
        elif check_meal_time['code'] == 500:
            return JSONResponse(status_code=500, content={'message': 'something went wrong - server'})

    # invalied meal time name
    elif mealTime != 'breakfast' or mealTime != 'lunch' or mealTime != 'dinner':
        return JSONResponse(status_code=404, content={'message': 'invalied meal-name'})

    # invalied time
    else:
        return JSONResponse(status_code=406, content={'message': 'invalied time'})


@route.get('/shopdetails', **doc['shopdetails'])
async def shopDetials(data=Depends(authontication.authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # get data from database and return
    shopData = db.get_shopdetails()
    if shopData == False:
        return JSONResponse(status_code=500, content={'message': 'something went wrong - server'})
    else:
        return JSONResponse(status_code=200, content={'message': 'successful', 'data': shopData})


@route.patch('/operationhold', **doc['operationhold'])
async def operationHold(data=Depends(authontication.authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unauthorized')
    # set current time
    timeZoon = pytz.timezone('Asia/Colombo')
    currentTime = datetime.now(timeZoon).time()
    # get shop details
    shopStatus = db.get_shopdetails_row()
    # check opening time and closing time
    if shopStatus['open_time'].time() < currentTime < shopStatus['close_time'].time():
        # udpate shop status accordingly
        status_update = db.update_shop_status(shopStatus['shutdown'])
        if status_update == True and shopStatus['shutdown'] == False:
            return JSONResponse(status_code=200, content={'message': 'successfuly open'})
        elif status_update == True and shopStatus['shutdown'] == True:
            return JSONResponse(status_code=200, content={'message': 'successfuly close'})
    else:
        return JSONResponse(status_code=400, content={'message': "cannot perform this operation while it's close time "})


# change shop opening and close time
@route.patch('/changeShopTime', **doc['changeShopTime'])
async def changeShopTime(shopTime: str = Query(description='which time you want to change', example='open_time | close_time'),
                         h: int = Query(
                             description='hours', gt=0, lt=24),
                         m: int = Query(
                             description='minuts', gt=0, lt=59),
                         data=Depends(authontication.authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # check shoptime variable
    if shopTime == 'open_time' or shopTime == 'close_time':
        # get stored data from database
        shopData = db.get_shopdetails_row()

        # time comparison with current time
        if shopTime == 'open_time':
            comparison = shopData['close_time'].time() < datetime(
                year=1970, month=1, day=1, hour=h, minute=m).time()
            if comparison == True:
                return JSONResponse(status_code=400, content={'message': 'you cannot set opening time conflicting with existing shop times.'})
        elif shopTime == 'close_time':
            comparison = shopData['open_time'].time() > datetime(
                year=1970, month=1, day=1, hour=h, minute=m).time()
            if comparison == True:
                return JSONResponse(status_code=400, content={'message': 'you cannot set close time conflicting with existing shop times.'})

        # update shop time
        shopTime = db.update_shop_time(shopTime, h, m)
        if shopTime == True:
            return JSONResponse(status_code=200, content={'message': 'successfull'})
        else:
            return JSONResponse(status_code=500, content={'message': 'something went wrong - server'})
    else:
        return JSONResponse(status_code=404, content={'message': 'time description is not matched'})
