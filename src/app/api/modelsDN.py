from uuid import uuid4

from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.databaseDN import Base


class Kosarica(Base):
    __tabelname__ = "kosarica"

    #atributi
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    imeKosarice = Column(String(20))

    #relacije/atrbuti drugje
    trgovine = relationship("Trgovina", back_populates="kosarica")


class Trgovina(Base):
    __tablename__ = "trgovina"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    imeTrgovine = Column(String(20))

    #relacije/atributi drugje
    izdelki = relationship("Izdelek", back_populates="trgovina")

    #Za to nism zihr če more met? 
    kosarica = relationship("Kosarica", back_populates="trgovine")


class Izdelek(Base):
    __tablename__ = "izdelek"

    #atributi
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    imeIzdelka = Column(String(50))
    cenaIzdelka = Column(Float)

    #relacije/atributi drugje
    trgovina = relationship("Trgovina", back_populates="izdelki")
