from fastapi import FastAPI
from bd.database import  engine, Base
from routers.movie import routerMovie
from routers.users import routerUser
from routers.cifra import routerCifra

# para ejecutar: uvicorn main:app --reload --port 4000

app = FastAPI(
    title='Aprendiendo FASTAPI',
    description='Primeros pasos API',
    version='0.0.1'
)

app.include_router(routerMovie)
app.include_router(routerUser)
app.include_router(routerCifra)

Base.metadata.create_all(bind=engine)










@app.get('/', tags=['Inicio'])
def read_root():
    return {'Hello':'World'}

