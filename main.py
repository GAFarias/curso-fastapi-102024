from fastapi import FastAPI
from bd.database import  engine, Base
from routers.movie import routerMovie
from routers.candy import routerCandy
from routers.users import routerUser
from routers.cifra import routerCifra
from routers.cifra_anterior import routerCifraAnterior
import uvicorn
import os

# para ejecutar: uvicorn main:app --reload --port 4000

app = FastAPI(
    title='Cifras Cines RealTime',
    description='Cifras de los cines para aplicacion gerencial',
    version='1.0.0'
)

app.include_router(routerMovie)
app.include_router(routerCandy)
app.include_router(routerUser)
app.include_router(routerCifra)
app.include_router(routerCifraAnterior)

Base.metadata.create_all(bind=engine)


@app.get('/', tags=['Inicio'])
def read_root():
    return {'APP':'GAFCines'}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

    

