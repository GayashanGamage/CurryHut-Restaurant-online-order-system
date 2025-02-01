from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from passlib.hash import pbkdf2_sha256
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends
from typing import Annotated

load_dotenv()
security = HTTPBearer()

# create JWT joken
def encodeToken(email, password, role):
    token = jwt.encode({'email' : email, 'password' : password, 'role' : role}, os.getenv('jwt_token'), algorithm='HS256')
    return token

# decode JWT token
def decodeToken(token):
    try:
        data = jwt.decode(token, os.getenv('jwt_token'), algorithms=['HS256'])
        return data
    except JWTError:
        return False


# encode password 
def encodePassword(plainPassword):
    encriptPassword = pbkdf2_sha256.hash(plainPassword)    
    return encriptPassword

# decode password
def decodePasword(palinPassword, encriptPassword):
    decriptedPassword = pbkdf2_sha256.verify(palinPassword, encriptPassword)
    return decriptedPassword

# deal with barer token
def authVerification(details : Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    return decodeToken(details.credentials)