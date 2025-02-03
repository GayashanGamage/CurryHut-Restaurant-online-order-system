from fastapi import APIRouter, Depends
from Dependencies import database, model
from fastapi.responses import JSONResponse
from Dependencies import authontication, email


route = APIRouter( tags=['adminAuth'])
db = database.get_database()

@route.post('/createAdminAccount')
async def createAdminUserAccount(userdetials : model.UserDetails ):
    # check dubplication email
    data = db.check_duplicate_admin_user(userdetials)
    if data == True:
        return JSONResponse(status_code=406, content="duplicated email" )
    else:
        # encript password
        userdetials.password = authontication.encodePassword(userdetials.password)
        # insert inew user data
        data = db.insert_admin_user(userdetials)
        if data['status'] == True:
            # send eamil - regardin to creation of new eamil
            emailData = email.sendEmail('Create new admin account', userdetials.email, 6)
            if emailData == True:
                return JSONResponse(status_code=200, content="successfull")
            elif emailData == False:
                return JSONResponse(status_code=500, content="email cannot send")
        elif data['code'] == 500:
            return JSONResponse(status_code=500, content="something go wrong")
        elif data['code'] == 401:
            return JSONResponse(status_code=401, content="invalied role")    
        


@route.get('/secreatecode')
async def createSereateCode(email_address : str):
    # crreate secreate code and update database
    data = db.update_secreate_code(email_address)
    if data['status'] == True:
        # send email with screate code 
        send_mail = email.sendEmail("secreate code for reset password", email_address, 7, code = {'code' : data['code']})
        if send_mail == True:
            return JSONResponse(status_code=200, content="successfull")
        elif send_mail == False:
            return JSONResponse(status_code=500, content="email cannot send")
    elif data['status'] == False:
        return JSONResponse(status_code=401, content="email not found")
    
@route.post('/login')
async def login(usercredencial : model.userCredencials):
    # get user data from database
    userDetails = db.get_credencials(usercredencial)
    # check user entered data with database data
    if userDetails != False:
        # decode password
        decoded = authontication.decodePasword(usercredencial.password, userDetails['password'])
        # validate password
        if decoded:
            # create and return JWT token
            token = authontication.encodeToken(usercredencial.email, usercredencial.password, usercredencial.role)
            return JSONResponse(status_code=200, content={'jwt_token' : token})
        # password invalied error
        else:
            return JSONResponse(status_code=406, content='password incorect')
    # email not found error
    elif userDetails == False:
        return JSONResponse(status_code=404, content='Credencials not valied')
    
@route.post('/codeverification')
async def codeverification(code : model.Code):
    # check user's secreate code and auto generate code are same or not
    data = db.check_secreate_code(code)
    if data['status'] == True:
        return JSONResponse(status_code=200, content='successfull')
    elif data['code'] == 401:
        return JSONResponse(status_code=401, content='unauthorized')
    elif data['code'] == 404:
        return JSONResponse(status_code=404, content='email not found')
      
@route.post('/resetpassword')
async def resetpassword(password : model.Password):
    # check whether user request to change password or not
    data = db.check_password_change(password)
    if data == True:
        # encript password
        encoded_password = authontication.encodePassword(password.password)
        # update password according to email
        update = db.change_password(password.email, encoded_password)
        if update == True:
            return JSONResponse(status_code=200, content='successfull')
        elif update == False:
            return JSONResponse(status_code=404, content='something went wrong')
    elif data == False:
        return JSONResponse(status_code=400, content='something went wrong')