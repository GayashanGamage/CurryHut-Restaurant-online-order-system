from fastapi import APIRouter, Depends, Query, Query
from Dependencies import authontication, model, database
from fastapi.responses import JSONResponse
from .docs.doc_menu import docs

db = database.get_database()

route = APIRouter(tags=['menu'], prefix='/menu')


@route.patch('/update', **docs['add'])
async def updateMenu(foods: model.Menu, data=Depends(authontication.authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # set updated datalist
    updateData = db.update_menu(foods)
    if updateData == True:
        # udpate menu status in shop details
        shop = db.update_menu_status()
        if shop == True:
            return JSONResponse(status_code=200, content={'message': 'successful'})
        else:
            return JSONResponse(status_code=500, content={'message': 'something went wrong - server'})
    else:
        return JSONResponse(status_code=500, content={'message': 'something went wrong - server'})


@route.patch('/set-availability', **docs['set-availability'])
async def setAvailability(id: str, data=Depends(authontication.authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # check the meal time
    meal_time = db.check_meal_time_by_id(id)
    if meal_time == True:
        update = db.update_availability(id)
        if update == True:
            return JSONResponse(status_code=200, content={"message": 'successful'})
        else:
            return JSONResponse(status_code=500, content={"message": "something went wrong - server"})
    else:
        return JSONResponse(status_code=400, content={"message": "cannot set availability for this item"})
