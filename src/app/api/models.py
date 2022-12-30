from pydantic import BaseModel, Field
from typing import List
from uuid import uuid4

#class za kosarico iz prejsne MS ima kosarica naslednje atribute
'''
 @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "imeKosarice")
    private String imeKosarice;

    ideja kako nardit v pythonu
    dodaj dict trgovin: 
        key: ime trgovine 
        value: dict izdelkov opisan spodaj

    potem pa lahko dodaš da je dict kjer je:
        key: ime izdelka 
        value: cena izdelka

    primer:

    dict trgovnine: 
    [
        key: Spar, value: dict 
            izdelki 
            [
                key: Spageti, value: 2,34
                key: Omaka, value: 4,23
                key: Rdeča Pesa, value: 1,76
                ... 
            ]

        key: Tuš, value: dict 
            izdelki 
            [
                key: Spageti, value: 2,34
                key: Omaka, value: 4,23
                key: Rdeča Pesa, value: 1,76
                ...
            ]
    ]

'''

#for testing purposes

#Nevem a bom mogu to uporabt al kako
class Izdelek(BaseModel): 
    #class za izdelek, kle bi lahko uporabu dict 
    # ampak nevem kako jih pol gnezdt
    izdlek_ime: str = Field(...)
    izdelek_cena: float = Field(...)

class Trgovina(BaseModel):
    imeTrgovine: str = Field(..., min_length=3, max_length=50)
    #izdelki: List[Izdelek] = Field(...)
    izdelki: str = Field(..., min_length=3, max_length=50)

class KosaricaSchema(BaseModel):
    imeKosarice: str = Field(..., min_length=3, max_length=50)
    #not sure če je to sploh prov
    #seznamTrgovin: List[Trgovina] = Field(...) 
    
    # za testiranje naj bo seznam samo nek string
    seznamTrgovin: list[Trgovina] = Field(...)

#ta podedjue vse od gor pa doda ID ???
class KosaricaDB(KosaricaSchema):
    id: int
