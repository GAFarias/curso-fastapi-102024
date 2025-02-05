from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from user_jwt import createToken

from fastapi import  Path, Query,Request,HTTPException,Depends
from typing import Optional
from fastapi.security import HTTPBearer
from bd.database import Session
from models.usuario import Usuario as ModelUsuario
from fastapi.encoders import jsonable_encoder





routerUser=APIRouter()

class User(BaseModel):
    email:str = Field(default="gaf")
    password:str = Field(default="12345")



# @routerUser.post('/login', tags=['authentication'])
# def login(user:User):
#     if user.email =='pepe' and user.password == '12345' :
#         token:str = createToken(user.dict())    
#         print(token)
#         return JSONResponse(content=token)



@routerUser.post('/login', tags=['authentication'])
def login(user:User):
    db = Session()
    data = db.query(ModelUsuario).filter(ModelUsuario.nombre == user.email and ModelUsuario.password == user.password).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Logueo incorrecto!!'})
    else:
        token:str = createToken(user.dict())    
        print(token)
        data.password=token
        # return JSONResponse(status_code=200,  content = [jsonable_encoder(data),token])
        return JSONResponse(content=token)
    # return JSONResponse(status_code=200,  content = jsonable_encoder(data))
        # loguea = Loguea(
        #     token=token, 
        #     empresa=data.empresa, 
        #     nivel=data.nivel
        # )
        # respuesta.token=token
        # respuesta.empresa=data.empresa
        # respuesta.nivel=data.nivel
        # return JSONResponse(content=token)
        # return JSONResponse(content=jsonable_encoder(loguea))
