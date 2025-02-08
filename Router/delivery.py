from fastapi import APIRouter, Depends, Path
from Dependencies.model import Delivery, delivery_update, delivery_status
from Dependencies import database
from fastapi.responses import JSONResponse
from Dependencies import authontication
from .docs.doc_delivery import doc

route = APIRouter(
    prefix="/delivery",
    tags=["delivery"]
)

db = database.get_database()


@route.post("/create", **doc['create'])
async def set_delivery(details: Delivery, data=Depends(authontication.authVerification)):
    # chacke whethere othorized person
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # find duplicate by name
    duplication = db.find_duplicate_location(details.place.lower())
    # if available send error
    if duplication == True:
        return JSONResponse(content={"message": "Place already exist"}, status_code=400)
    # if not duplicated
    elif duplication == False:
        # otherwise create new delivery location
        data_insertion = db.insert_delivery_place(details)
        if data_insertion == True:
            return JSONResponse(content={"message": "Success"}, status_code=200)
        elif data_insertion == False:
            return JSONResponse(content={"message": "something went wrong"}, status_code=500)


# this is no need to authonticate
@route.get("/get", **doc['get'])
async def get_delivery():
    store_data = db.get_delivery_place()
    if store_data == False:
        return JSONResponse(content={"data": []}, status_code=400)
    else:
        return JSONResponse(content={'data': store_data}, status_code=200)


@route.put("/update", **doc['update'])
async def update_delivery(details: delivery_update, data=Depends(authontication.authVerification)):
    # chacke whethere othorized person
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # check duplication by name and id
    duplication = db.find_duplication_location_for_update(
        details.place.lower(), details.id)
    if duplication == True:
        return JSONResponse(status_code=400, content={"message": "delivery place cannot duplicated"})
    elif duplication == False:
        # update database
        update = db.update_delivery_location(
            details.cost, details.place, details.id, details.updated_at)
        if update == True:
            return JSONResponse(status_code=200, content={'message': 'Success'})
        else:
            return JSONResponse(status_code=500, content={'message': 'database cannot update - server'})


@route.post('/set-status', **doc['set-status'])
async def deliver_status(details: delivery_status, data=Depends(authontication.authVerification)):
    # chacke whethere othorized person
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content={"message": 'unathorized'})
    store_data = db.update_delivery_status(details)
    if store_data:
        return JSONResponse(content={"message": "Success"}, status_code=200)
    else:
        return JSONResponse(content={"message": "Failed"}, status_code=400)


@route.delete("/delete/{id}")
async def delete_delivery(id: str = Path(description="delivery id"),
                          data=Depends(authontication.authVerification)):
    # chacke whethere othorized person
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    store_data = db.delete_delivery(id)
    if store_data:
        return JSONResponse(content={"message": "Success"}, status_code=200)
    else:
        return JSONResponse(content={"message": "Failed"}, status_code=500)
