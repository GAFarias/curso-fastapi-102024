from bd.database import Base  #Importo desde la carpeta bd

from sqlalchemy import Column, Integer, String, Float

class Empresa(Base):
    __tablename__ = 'empresa'
    id = Column( Integer, primary_key=True)
    cod_empresa = Column(Integer)
    cod_cine = Column(Integer)
    nombre_cine = Column(String)
    tiene_candy = Column(Integer)



