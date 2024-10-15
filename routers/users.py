from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from user_jwt import createToken


routerUser=APIRouter()

class User(BaseModel):
    email:str
    password:str



@routerUser.post('/login', tags=['authentication'])
def login(user:User):
    if user.email =='pepe' and user.password == '12345' :
        token:str = createToken(user.dict())    
        print(token)
        return JSONResponse(content=token)