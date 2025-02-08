from fastapi import  Path, Query,Request,HTTPException,Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import validateToken
from fastapi.security import HTTPBearer
from bd.database import Session
from models.empresa import Empresa as ModelEmpresa
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from models.usuario import Usuario as ModelUsuario

routerEmpresa=APIRouter()

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data=validateToken(auth.credentials)
        # Busca si el usuario es valido:
        db = Session()
        datausr = db.query(ModelUsuario).filter(ModelUsuario.nombre == data['email'] and ModelUsuario.password == data['password']).first()
        if datausr is None:      
            raise HTTPException(status_code=403, detail='Credenciales incorrectas')

class Empresa(BaseModel):
        id:Optional[int] = None
        cod_empresa: int = Field(ge=1 , le=999) 
        cod_cine: int = Field(ge=1 , le=999) 
        nombre_cine: int = Field(default='Nombre del Cine',min_length=2, max_length=50)
        tiene_candy: int = Field(ge=0 , le=1) 


@routerEmpresa.get('/empresas', tags=['Empresas'])  #, dependencies=[Depends(BearerJWT())])
def get_empresas():
    db = Session()
    data = db.query(ModelEmpresa).all()
    return JSONResponse( content = jsonable_encoder(data))



@routerEmpresa.get('/empresas/{id}', tags=['Empresas'], status_code=200)
def get_empresas(id: int = Path(ge=1 , le=999)):
    db = Session()
    data = db.query(ModelEmpresa).filter(ModelEmpresa.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    return JSONResponse(status_code=200,  content = jsonable_encoder(data))


@routerEmpresa.get('/empresas_cines/{cod_empresa}', tags=['Empresas'], status_code=200)
def get_empresas_by_empresa(cod_empresa: int = Path(ge=1, le=999)):
    db = Session()
    data = db.query(ModelEmpresa).filter(ModelEmpresa.cod_empresa == cod_empresa).all()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    return JSONResponse(status_code=200,  content = jsonable_encoder(data))
 

@routerEmpresa.post('/empresas', tags=['Empresas'])
def create_empresa(empresa : Empresa):
    # empresas.append(empresa)
    # #return empresa.title
    db = Session()
    newEmpresa = ModelEmpresa( **empresa.dict())  # el doble ** significa pasar todos los argumentos
    db.add(newEmpresa)
    db.commit()
    return JSONResponse(content={'message': 'Se ha creado una nueva Empresa'} )

@routerEmpresa.put('/empresas/{id}', tags=['Empresas'])
def update_empresas(id: int, empresa: Empresa): 
    db = Session()
    data = db.query(ModelEmpresa).filter(ModelEmpresa.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    
    data.cod_empresa = empresa.cod_empresa
    data.cod_cine = empresa.cod_cine
    data.nombre_cine = empresa.nombre_cine
    data.tiene_candy = empresa.tiene_candy
    
    db.commit()
    return JSONResponse(status_code=200, content={'message': 'Modificacion exitosa'})



@routerEmpresa.delete('/empresas/{id}', tags=['Empresas'])
def delete_empresa(id:int):
    db = Session()
    data = db.query(ModelEmpresa).filter(ModelEmpresa.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    db.delete(data)
    db.commit()
    return JSONResponse(content={'message': 'Recurso eliminado'})
