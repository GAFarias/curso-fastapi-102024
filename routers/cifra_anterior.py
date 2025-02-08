from fastapi import  Path, Query,Request,HTTPException,Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import validateToken
from fastapi.security import HTTPBearer
from bd.database import Session
from models.cifras_anteriores import CifraAnterior as ModelCifraAnterior
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from models.usuario import Usuario as ModelUsuario

routerCifraAnterior=APIRouter()

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data=validateToken(auth.credentials)
        # Busca si el usuario es valido:
        db = Session()
        datausr = db.query(ModelUsuario).filter(ModelUsuario.nombre == data['email'] and ModelUsuario.password == data['password']).first()
        if datausr is None:      
            raise HTTPException(status_code=403, detail='Credenciales incorrectas')

class CifraAnterior(BaseModel):
        id:Optional[int] = None
        idCine : int = Field(default=1)
        Dia : int = Field(default=0)
        Mes : int = Field(default=0)
        Anio : int = Field(default=0)
        CodPelicula  : str = Field(default='0',min_length=5, max_length=20)
        NomPelicula  : str = Field(default='Nombre de la pelicula',min_length=2, max_length=100)
        Precio: float = Field(default=0.0)
        Tot : int = Field(default=1)



# @routerCifra.get('/cifras', tags=['Cifras'], dependencies=[Depends(BearerJWT())])
@routerCifraAnterior.get('/cifrasanteriores', tags=['CifrasAnteriores'])
def get_cifras_anteriores():
    db = Session()
    data = db.query(ModelCifraAnterior).all()
    return JSONResponse( content = jsonable_encoder(data))



@routerCifraAnterior.get('/cifrasanteriores/{id}', tags=['CifrasAnteriores'], status_code=200)
def get_cifras_anteriores(id: int = Path(ge=1 , le=100)):
    db = Session()
    data = db.query(ModelCifraAnterior).filter(ModelCifraAnterior.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    return JSONResponse(status_code=200,  content = jsonable_encoder(data))


 

@routerCifraAnterior.post('/cifrasanteriores', tags=['CifrasAnteriores'])
def create_cifra_anterior(cifra_anterior : CifraAnterior):
    # movies.append(movie)
    # #return movie.title
    db = Session()
    newCifraAnterior = ModelCifraAnterior( **cifra_anterior.dict())  # el doble ** significa pasar todos los argumentos
    db.add(newCifraAnterior)
    db.commit()
    return JSONResponse(content={'message': 'Se ha creado una nueva cifra Anterior'} )


@routerCifraAnterior.delete('/cifrasanteriores/{idCine}', tags=['CifrasAnteriores'])
def delete_cifra_anterior(idCine:int):
    db = Session()
    data = db.query(ModelCifraAnterior).filter(ModelCifraAnterior.idCine == idCine).all()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    # db.delete(data)
    # Iterar sobre los objetos y eliminarlos uno por uno
    for cifraanterior in data:
        db.delete(cifraanterior)
        
    db.commit()
    return JSONResponse(content={'message': 'Cifras Anteriores del cine eliminadas'})
