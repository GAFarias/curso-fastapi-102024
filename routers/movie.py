from fastapi import  Path, Query,Request,HTTPException,Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import validateToken
from fastapi.security import HTTPBearer
from bd.database import Session
from models.movie import Movie as ModelMovie
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from models.usuario import Usuario as ModelUsuario

routerMovie=APIRouter()

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data=validateToken(auth.credentials)
        db = Session()
        datos = db.query(ModelUsuario).filter(ModelUsuario.nombre == data['email'] and ModelUsuario.password == data['password']).first()
        if not datos:
            raise HTTPException(status_code=403, detail='Credenciales incorrectas')
        # if data['email'] != 'gaf':
        #     raise HTTPException(status_code=403, detail='Credenciales incorrectas')

class Movie(BaseModel):
        id:Optional[int] = None
        title: str = Field(default='Titulo de la pelicula',min_length=3, max_length=60)
        overview: str = Field(default='Descripcion de la pelicula',min_length=5, max_length=200)
        year: int = Field(default=1980)
        rating: int = Field(ge=1 , le=10)  # es un rango de 1 a 10
        category: str = Field(default='Categoria de la pelicula',min_length=5, max_length=50)


@routerMovie.get('/movies', tags=['Peliculas'], dependencies=[Depends(BearerJWT())])
def get_movies():
    db = Session()
    data = db.query(ModelMovie).all()
    return JSONResponse( content = jsonable_encoder(data))



@routerMovie.get('/movies/{id}', tags=['Peliculas'], status_code=200)
def get_movies(id: int = Path(ge=1 , le=100)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    return JSONResponse(status_code=200,  content = jsonable_encoder(data))


@routerMovie.get('/movies/', tags=['Peliculas'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=50)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.category == category).all()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    return JSONResponse(status_code=200,  content = jsonable_encoder(data))
 

@routerMovie.post('/movies', tags=['Peliculas'])
def create_movie(movie : Movie):
    # movies.append(movie)
    # #return movie.title
    db = Session()
    newMovie = ModelMovie( **movie.dict())  # el doble ** significa pasar todos los argumentos
    db.add(newMovie)
    db.commit()
    return JSONResponse(content={'message': 'Se ha creado una nueva pelicula'} )

@routerMovie.put('/movies/{id}', tags=['Peliculas'])
def update_movies(id: int, movie: Movie): 
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    
    data.title = movie.title
    data.overview = movie.overview
    data.rating = movie.rating
    data.year = movie.year
    data.category = movie.category
    db.commit()
    return JSONResponse(status_code=200, content={'message': 'Modificacion exitosa'})



@routerMovie.delete('/movies/{id}', tags=['Peliculas'])
def delete_movie(id:int):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    db.delete(data)
    db.commit()
    return JSONResponse(content={'message': 'Recurso eliminado'})
