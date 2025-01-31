from fastapi import  Path, Query,Request,HTTPException,Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import validateToken
from fastapi.security import HTTPBearer
from bd.database import Session
from models.candy import Candy as ModelCandy
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter

routerCandy=APIRouter()

# class BearerJWT(HTTPBearer):
#     async def __call__(self, request: Request):
#         auth = await super().__call__(request)
#         data=validateToken(auth.credentials)
#         if data['email'] != 'pepe':
#             raise HTTPException(status_code=403, detail='Credenciales incorrectas')

class Candy(BaseModel):
        id:Optional[int] = None
        idCine : int = Field(default=1)
        cajaNro : int = Field(default=1)
        Fecha : str = Field(default='Fecha de la funcion',min_length=5, max_length=10)
        FormaPago  : str = Field(default='Forma de Pago',min_length=1, max_length=10)
        Total: float = Field(default=0.0)
        UltActu : str = Field(default='20250101120000',min_length=5, max_length=20)


# @routerCifra.get('/cifras', tags=['Cifras'], dependencies=[Depends(BearerJWT())])
@routerCandy.get('/candy', tags=['Candys'])
def get_candys():
    db = Session()
    data = db.query(ModelCandy).all()
    return JSONResponse( content = jsonable_encoder(data))



@routerCandy.get('/candys/{idCine}', tags=['Candys'], status_code=200)
def get_candys(idCine: int = Path(ge=1 , le=99999)):
    db = Session()
    data = db.query(ModelCandy).filter(ModelCandy.idCine == idCine).all()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    return JSONResponse(status_code=200,  content = jsonable_encoder(data))


 

@routerCandy.post('/candys', tags=['Candys'])
def create_candy(candy : Candy):
    # movies.append(movie)
    # #return movie.title
    db = Session()
    newCandy = ModelCandy( **candy.dict())  # el doble ** significa pasar todos los argumentos
    db.add(newCandy)
    db.commit()
    return JSONResponse(content={'message': 'Se ha creado un nuevo mov de Candy'} )


@routerCandy.delete('/candys/{idCine}', tags=['Candys'])
def delete_candy(idCine:int):
    db = Session()
    data = db.query(ModelCandy).filter(ModelCandy.idCine == idCine).all()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    # db.delete(data)
    # Iterar sobre los objetos y eliminarlos uno por uno
    for candy in data:
        db.delete(candy)
        
    db.commit()
    return JSONResponse(content={'message': 'Mov Candy del cine eliminados'})
