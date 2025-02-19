from bd.database import Base  #Importo desde la carpeta bd

from sqlalchemy import Column, Integer, String, Float

class CifraAnterior(Base):
    __tablename__ = 'cifra_anterior'
    id = Column( Integer, primary_key=True)
    idCine = Column(Integer)
    Dia = Column(Integer)
    Mes = Column(Integer)
    Anio = Column(Integer)
    CodPelicula = Column(String)
    NomPelicula = Column(String)
    Precio = Column(Float)
    Tot = Column(Integer)
    TotWeb = Column(Integer)
    