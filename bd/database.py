import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


sqliteName = 'movies.sqlite'
base_dir = os.path.dirname(os.path.realpath(__file__))
datebaseUrl = f"sqlite:///{os.path.join(base_dir, sqliteName)}"

engine = create_engine(datebaseUrl, echo=True)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Cambia el nombre a SessionLocal
# Session = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():  # Función para obtener la sesión (¡clave!)
    db = Session()
    try:
        yield db
    finally:
        db.close()