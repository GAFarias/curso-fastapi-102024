from fastapi import  Path, Query,Request,HTTPException,Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import validateToken
from fastapi.security import HTTPBearer
from bd.database import Session
from models.cifras import Cifra as ModelCifra
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from models.usuario import Usuario as ModelUsuario

routerCifra=APIRouter()

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data=validateToken(auth.credentials)
        # Busca si el usuario es valido:
        db = Session()
        datausr = db.query(ModelUsuario).filter(ModelUsuario.nombre == data['email'] and ModelUsuario.password == data['password']).first()
        if datausr is None:      
            raise HTTPException(status_code=403, detail='Credenciales incorrectas')

class Cifra(BaseModel):
        id:Optional[int] = None
        idCine : int = Field(default=1)
        Fecha : str = Field(default='Fecha de la funcion',min_length=5, max_length=10)
        Hora  : str = Field(default='Hora de la funcion',min_length=2, max_length=5)
        Sala : int = Field(default=1)
        Lenguaje  : str = Field(default='Cast',min_length=2, max_length=20)
        Tipo  : str = Field(default='ATP',min_length=2, max_length=20)
        CodPelicula  : str = Field(default='0',min_length=5, max_length=20)
        NomPelicula  : str = Field(default='Nombre de la pelicula',min_length=2, max_length=100)
        Precio: float = Field(default=0.0)
        Tot : int = Field(default=0)
        TotWeb : int = Field(default=0)
        UltActu : str = Field(default='20250101120000',min_length=5, max_length=20)


# @routerCifra.get('/cifras', tags=['Cifras'], dependencies=[Depends(BearerJWT())])
@routerCifra.get('/cifras', tags=['Cifras'])
def get_cifras():
    db = Session()
    data = db.query(ModelCifra).all()
    return JSONResponse( content = jsonable_encoder(data))



# @routerCifra.get('/cifras/{id}', tags=['Cifras'], status_code=200)
# def get_cifras(id: int = Path(ge=1 , le=100)):
#     db = Session()
#     data = db.query(ModelCifra).filter(ModelCifra.id == id).first()
#     if not data:
#         return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
#     return JSONResponse(status_code=200,  content = jsonable_encoder(data))

@routerCifra.get('/cifras/{idCine}', tags=['Cifras'], status_code=200)
def get_cifras(idCine: int = Path(ge=1 , le=99999)):
    db = Session()
    data = db.query(ModelCifra).filter(ModelCifra.idCine == idCine).all()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    return JSONResponse(status_code=200,  content = jsonable_encoder(data))


 

@routerCifra.post('/cifras', tags=['Cifras'])
def create_cifra(cifra : Cifra):
    # movies.append(movie)
    # #return movie.title
    db = Session()
    newCifra = ModelCifra( **cifra.dict())  # el doble ** significa pasar todos los argumentos
    db.add(newCifra)
    db.commit()
    return JSONResponse(content={'message': 'Se ha creado una nueva cifra'} )


@routerCifra.delete('/cifras/{idCine}', tags=['Cifras'])
def delete_cifra(idCine:int):
    db = Session()
    data = db.query(ModelCifra).filter(ModelCifra.idCine == idCine).all()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    # db.delete(data)
    # Iterar sobre los objetos y eliminarlos uno por uno
    for cifra in data:
        db.delete(cifra)
        
    db.commit()
    return JSONResponse(content={'message': 'Cifras del cine eliminadas'})
