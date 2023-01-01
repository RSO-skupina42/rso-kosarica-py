from pydantic import BaseModel, Field
from typing import List
from uuid import uuid4


#Shema za izdelke 

#base class
class IzdelekBase(BaseModel):  
    # ampak nevem kako jih pol gnezdt
    imeIzdelka: str
    cenaIzdelka: float
    trgovnina: str

#Create class
class IzdelekCreate(IzdelekBase): 
    pass

#končni class
class Izdelek(IzdelekBase): 
    id: int
    kosarica_id: int 
    
    #To je da se lahko vrine v Košarico?
    class Config:
        orm_mode = True



#Shema za košarico 

#base class
class KosaricaBase(BaseModel):
    imeKosarice: str 
    
#create class
class KosaricaCreate(KosaricaBase):
    pass

#koncni class
class Kosarica(KosaricaBase):
    id: int 
    izdelki: list[Izdelek] = []

    class Config:
        orm_mode = True

#update class ??
class KosaricaUpdate(KosaricaBase):
    izdelki: list[Izdelek] = []

    class Config:
        orm_mode = True

