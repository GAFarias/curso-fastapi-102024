from bd.database import Base  #Importo desde la carpeta bd

from sqlalchemy import Column, Integer, String, Float

class Cifra(Base):
    __tablename__ = 'cifras'
    id = Column( Integer, primary_key=True)
    idCine = Column(Integer)
    Fecha = Column(String )
    Hora = Column(String)
    Sala = Column(Integer)
    Lenguaje = Column(String)
    Tipo = Column(String)
    CodPelicula = Column(String)
    NomPelicula = Column(String)
    Precio = Column(Float)
    Tot = Column(Integer)
    TotWeb = Column(Integer)
    UltActu = Column(String)