from fastapi import APIRouter, Depends
from Dependencies import database, authontication, model, sms
from fastapi.responses import JSONResponse
from random import randint
from .docs.doc_rider import doc

db = database.get_database()
route = APIRouter(tags=['Rider'], prefix='/rider')


@route.patch('/numberVerification/', **doc['numberVerification'])
async def riderNumberVerification(details: model.RiderVerification, data=Depends(authontication.authVerification)):
    # id == None ? new rider, id != None ? update existing rider's
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    else:
        # generate secreate code on rider's details ( database )
        send_code = db.store_secreate_code(details)
        if send_code == False:
            return JSONResponse(status_code=400, content={"message": 'riders information not found'})
        elif send_code == True:
            # send verification code to the rider's mobile
            send_verification = sms.sendSMS(
                details.mobile, f'Hi {details.first_name}. This is CURRY-HUT Narahenpita and This is for confirm your mobile number. code is {details.secreate_code}')
            if send_verification == True:
                return JSONResponse(status_code=200, content={"message": 'successfull'})

            elif send_verification == False:
                return JSONResponse(status_code=503, content={"message": 'sms cannot send due to service providers errro'})


@route.post('/add', **doc['add'])
async def addRider(rider: model.Rider, data=Depends(authontication.authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # find duplication of the rider details
    duplicate_rider = db.check_duplicate_rider(rider)
    if duplicate_rider == False:
        # store data in the database
        store_rider = db.insert_rider(rider)
        if store_rider == True:
            # send verification code to the rider's mobile
            send_verification = sms.sendSMS(
                rider.mobile, f'Hi {rider.first_name}. This is CURRY-HUT Narahenpita and This is for confirm your mobile number. code is {rider.secreate_code}')
            if send_verification == True:
                return JSONResponse(status_code=200, content='successfull')
            else:
                return JSONResponse(status_code=503, content={'message': 'sms cannot send'})
        elif store_rider == False:
            return JSONResponse(status_code=500, content={'message': 'something went wrong - server'})
    elif duplicate_rider == True:
        return JSONResponse(status_code=400, content={'message': 'some or all rider details alreddy in the system'})


@route.delete('/delete/{id}', **doc['delete'])
async def removeRider(id: str, data=Depends(authontication.authVerification)):
    # perpose : delete rider if he compleate all deliveries and return to the shop
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # check he is on the way to deliver
    order_status = db.compleate_all_orders(id)
    if order_status == True:
        # remove rider
        remove_rider = db.remove_rider(id)
        if remove_rider == True:
            return JSONResponse(status_code=200, content={'message': 'successfull'})
        else:
            return JSONResponse(status_code=500, content={"message": 'something went wrong - server'})
    elif order_status == False:
        return JSONResponse(status_code=401, content={'message': 'rider cannot remove - on the way to deliver'})


@route.delete('/deleteforce/', **doc['deleteforce'])
async def removeRiderForce(rider_data: model.RiderDeleteForce, data=Depends(authontication.authVerification)):
    # perposer : delete rider using authonticated password
    # when : '/rider/delete/{id}' is 401
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # check the password with jwt token's password
    if rider_data.password != data['password']:
        return JSONResponse(status_code=401, content='unathorized')
    elif rider_data.password == data['password']:
        # delete rider
        rider = db.remove_rider(rider_data.id)
        if rider == True:
            return JSONResponse(status_code=200, content={"message": 'successfull'})
        else:
            return JSONResponse(status_code=500, content={"message": 'something went wrong - server'})


@route.patch('/update/', **doc['update'])
async def updateRider(details: model.RiderContactUpdate, data=Depends(authontication.authVerification)):
    # perpose : update rider's contact number only ( not other details )
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    else:
        # update contact number
        update_contact = db.update_rider_contact(details)
        if update_contact == True:
            send_sms = sms.sendSMS(
                details.new_mobile, f'Hi {details.first_name}. as a rider crew, you change your new mobile number to {details.new_mobile} from {details.old_mobile}')
            if send_sms == True:
                return JSONResponse(status_code=200, content={'message': 'successful'})
            else:
                return JSONResponse(status_code=503, content={"message": 'message cannot send - server'})
        else:
            return JSONResponse(status_code=500, content={"message": 'something went wrong - server'})


@route.patch('/log', **doc['log'])
async def riderLog(id: str, data=Depends(authontication.authVerification)):
    # perpose : update rider's log status
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    else:
        # check all oders are compleated and return to the shop when log off
        status = db.orders_compleated_and_return(id)
        if status == True:
            # switch log status
            switch_log = db.switch_rider_log(id)
            if switch_log == True:
                # TODO: send generated auto login link via SMS
                return JSONResponse(status_code=200, content={"message": 'successful'})
            else:
                return JSONResponse(status_code=500, content={"message": 'something went wrong - server'})
        elif status == False:
            return JSONResponse(status_code=400, content={"message": 'rider cannot log off - on the way to deliver'})


@route.get('/all', **doc['all'])
async def getAllRiders(data=Depends(authontication.authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    else:
        # get all riders
        riders_data = db.get_all_riders()
        if riders_data == False:
            return JSONResponse(status_code=400, content={"message": 'no riders found'})
        else:
            return JSONResponse(status_code=200, content={"message": 'successful', 'data': riders_data})
