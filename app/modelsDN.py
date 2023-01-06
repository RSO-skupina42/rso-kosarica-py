from uuid import uuid4

from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from .databaseDN import Base


class Kosarica(Base):
    __tablename__ = "kosarica"

    #atributi
    id = Column(Integer, primary_key=True, index=True)
    imeKosarice = Column(String(20))

    #relacije/atrbuti drugje
    izdelki = relationship("Izdelek", back_populates="kosarica")


class Izdelek(Base):
    __tablename__ = "izdelek"

    #atributi
    id = Column(Integer, primary_key=True, index=True)
    imeIzdelka = Column(String(50))
    cenaIzdelka = Column(Float)
    trgovnina = Column(String(20))

    
    #relacije/atributi drugje
    kosarica_id = Column(Integer, ForeignKey('kosarica.id'))
    kosarica = relationship("Kosarica", back_populates="izdelki")
    
