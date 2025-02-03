from fastapi import APIRouter, Depends
from Dependencies.model import Delivery, delivery_update, delivery_status
from Dependencies import database
from fastapi.responses import JSONResponse

route = APIRouter(
    prefix="/delivery",
    tags=["delivery"]
)

db = database.get_database()

@route.post("/create")
async def set_delivery(details : Delivery):
    # check duplicated names
    places = db.check_delivery_duplicate(details.place)
    if places['status'] == True:
        return JSONResponse(content={"status" : "Failed", "message" : "Place already exist"}, status_code=400)
    else:
        # insert new place
        store_data = db.insert_delivery_place(details)
        if store_data:
            return JSONResponse(content={"status" : "Success"}, status_code=200)
        else:
            return JSONResponse(content={"status" : "Failed"}, status_code=400)
    
@route.get("/get")
async def get_delivery():
    store_data = db.get_delivery_place()
    return JSONResponse(content=store_data, status_code=200)

@route.put("/update")
async def update_delivery(details : delivery_update):
    # get duplicate delivery places
    places = db.check_delivery_duplicate(details.place)
    if places['status'] == True:
        # check if the place is the same as the one being updated
        if places['data'][0]['_id'] != details.id:
            return JSONResponse(content={"status" : "Failed", "message" : "Place already exist"}, status_code=400)
    else:
        store_data = db.update_delivery_details(details)
        if store_data:
            return JSONResponse(content={"status" : "Success"}, status_code=200)
        else:
            return JSONResponse(content={"status" : "Failed"}, status_code=500)

@route.post('/set-status')
async def deliver_status( details : delivery_status):
    store_data = db.update_delivery_status(details)
    if store_data:
        return JSONResponse(content={"status" : "Success"}, status_code=200)
    else:
        return JSONResponse(content={"status" : "Failed"}, status_code=400)
    

@route.delete("/delete/{id}")
async def delete_delivery(id : str):
    store_data = db.delete_delivery(id)
    if store_data:
        return JSONResponse(content={"status" : "Success"}, status_code=200)
    else:
        return JSONResponse(content={"status" : "Failed"}, status_code=400)
    