from fastapi import  Path, Query,Request,HTTPException,Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import validateToken
from fastapi.security import HTTPBearer
from bd.database import Session
from models.usuario import Usuario as ModelUsuario
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter

routerUsuario=APIRouter()

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data=validateToken(auth.credentials)
        # Busca si el usuario es valido:
        db = Session()
        datausr = db.query(ModelUsuario).filter(ModelUsuario.nombre == data['email'] and ModelUsuario.password == data['password']).first()
        if datausr is None:      
            raise HTTPException(status_code=403, detail='Credenciales incorrectas')




class Usuario(BaseModel):
        id:Optional[int] = None
        nombre: str = Field(default='Nombre del Usr',min_length=3, max_length=60)
        password: str = Field(default='Clave del usr',min_length=5, max_length=20)
        empresa: int = Field(default=1)
        nivel: int = Field(ge=1 , le=10)  # es un rango de 1 a 10
        


@routerUsuario.get('/usuarios', tags=['Usuarios']) #, dependencies=[Depends(BearerJWT())])
def get_usuarios():
    db = Session()
    data = db.query(ModelUsuario).all()
    return JSONResponse( content = jsonable_encoder(data))



@routerUsuario.get('/usuarios/{id}', tags=['Usuarios'], status_code=200)
def get_usuarios(id: int = Path(ge=1 , le=100)):
    db = Session()
    data = db.query(ModelUsuario).filter(ModelUsuario.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    return JSONResponse(status_code=200,  content = jsonable_encoder(data))


# @routerUsuario.get('/usuarios/', tags=['Usuarios'])
# def get_usuarios_by_category(category: str = Query(min_length=5, max_length=50)):
#     db = Session()
#     data = db.query(ModelUsuario).filter(ModelUsuario.category == category).all()
#     if not data:
#         return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
#     return JSONResponse(status_code=200,  content = jsonable_encoder(data))
 

@routerUsuario.post('/usuarios', tags=['Usuarios'])
def create_usuario(usuario : Usuario):
    # msuarios.append(msuario)
    # #return msuario.title
    db = Session()
    newUsuario = ModelUsuario( **usuario.dict())  # el doble ** significa pasar todos los argumentos
    db.add(newUsuario)
    db.commit()
    return JSONResponse(content={'message': 'Se ha creado un nuevo usuario'} )

@routerUsuario.post('/usuarios_admin/{clave}', tags=['Usuarios'])
def create_usuario_admin(clave:str):
    if clave=="saitam0409-":
        db = Session()
        data = db.query(ModelUsuario).filter(ModelUsuario.nombre == 'admin').first()
        if data:
            db.delete(data)
            db.commit()
        newUsuario = ModelUsuario( )  # el doble ** significa pasar todos los argumentos
        newUsuario.nombre="admin"
        newUsuario.password="12345"
        newUsuario.nivel=9
        newUsuario.empresa=0
        db.add(newUsuario)
        db.commit()
        return JSONResponse(content={'message': 'Se ha creado un nuevo administrador'} )
    return JSONResponse(content={'message': 'No se hizo nada'} )
    

@routerUsuario.put('/usuarios/{id}', tags=['Usuarios'])
def update_usuarios(id: int, usuario: Usuario): 
    db = Session()
    data = db.query(ModelUsuario).filter(ModelUsuario.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    
    data.nombre = usuario.nombre
    data.password = usuario.password
    data.empresa = usuario.empresa
    data.nivel = usuario.nivel
    db.commit()
    return JSONResponse(status_code=200, content={'message': 'Modificacion exitosa'})



@routerUsuario.delete('/usuarios/{id}', tags=['Usuarios'])
def delete_usuario(id:int):
    db = Session()
    data = db.query(ModelUsuario).filter(ModelUsuario.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    db.delete(data)
    db.commit()
    return JSONResponse(content={'message': 'Recurso eliminado'})
