from pydantic import BaseModel, Field
from typing import List
from uuid import uuid4


#Shema za izdelke 

#base class
class IzdelekBase(BaseModel):  
    # ampak nevem kako jih pol gnezdt
    izdlek_ime: str
    izdelek_cena: float 

#Create class
class IzdelekCreate(IzdelekBase): 
    id: int
    #not sure zakaj pass
    pass

#končni class
class Izdelek(IzdelekBase): 
    id: int

    #To je da se lahko vrine v trgovino?
    class Config:
        orm_mode = True


#Shema za trgovine 

#base class
class TrgovinaBase(BaseModel):
    imeTrgovine: str 

#create class
class TrgovinaCreate(TrgovinaBase):
    id:int
    pass

#koncni class?
class Trgovina(TrgovinaBase):
    id:int
    izdelki: List[Izdelek] = []

    class Config:
        orm_mode = True

#update class
class TrgovinaUpdate(TrgovinaBase):
    izdelki: List[Izdelek] = []

    class Config:
        orm_mode = True


#Shema za košarico 

#base class
class KosaricaBase(BaseModel):
    imeKosarice: str 
    
#create class
class KosaricaCreate(KosaricaBase):
    id: int
    pass

#koncni class
class Kosarica(KosaricaBase):
    id: int 
    trgovine = List[Trgovina] = []

    class Config:
        orm_mode = True

#update class
class KosaricaUpdate(KosaricaBase):
    trgovine: List[Trgovina] = []

    class Config:
        orm_mode = True


