from bd.database import Base  #Importo desde la carpeta bd

from sqlalchemy import Column, Integer, String, Float

class Candy(Base):
    __tablename__ = 'candys'
    id = Column( Integer, primary_key=True)
    idCine = Column(Integer)
    quePuesto = Column(Integer)
    cajaNro = Column(Integer)
    Usuario = Column(String )
    Fecha = Column(String )
    FormaPago = Column(String)
    Total = Column(Float)
    UltActu = Column(String)