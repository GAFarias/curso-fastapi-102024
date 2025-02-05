from bd.database import Base  #Importo desde la carpeta bd

from sqlalchemy import Column, Integer, String, Float

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column( Integer, primary_key=True)
    nombre = Column(String)
    password = Column(String)
    empresa = Column(Integer)
    nivel = Column(Integer)
    


