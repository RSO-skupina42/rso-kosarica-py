from typing import List

from fastapi import APIRouter, HTTPException, Path, Depends, FastAPI

from sqlalchemy.orm import Session

import crudDN, modelsDN
import schemasDN


from databaseDN import SessionLocal, engine


app = FastAPI()

modelsDN.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#dobi vse košarices
@app.get("/", response_model=List[schemasDN.Kosarica])
async def read_all_kosarice(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crudDN.get_all_kosarice(db, skip=skip, limit=limit)


#ustavri novo košarico
@app.post("/", response_model=schemasDN.Kosarica)
async def create_kosarica(kosarica: schemasDN.KosaricaCreate, db: Session = Depends(get_db)):
    db_kosarica = crudDN.get_kosarica(db, imeKosarice=kosarica.imeKosarice)
    #print(db_kosarica.imeKosarice)
    if db_kosarica:
        raise HTTPException(status_code=400, detail="Kosarica ze obstaja")
    return crudDN.create_kosarica(db=db, kosarica=kosarica)


#za testiranje 
@app.get("/{id}")
async def get_kosarica(id: int):
    return f"This is the id that was sent through {id}."

@app.post("/kosarice/{kosarica_id}/izdelki/", response_model=schemasDN.Izdelek)
def create_izdelek_for_kosarica(kosarica_id: int, izdelek: schemasDN.IzdelekCreate, db: Session = Depends(get_db)):
    return crudDN.create_izdelek_kosarico(db=db, izdelek=izdelek, kosarica_id=kosarica_id)




########stare operacije 
'''@router.post("/", response_model=KosaricaDB, status_code=201)
async def create_kosarica(payload: KosaricaSchema):
    kosarica_id = await crud.post(payload)

    response_object = {
        "id": kosarica_id,
        "imeKosarice": payload.imeKosarice,
        "seznamTrgovin": payload.seznamTrgovin,
    }

    return response_object


@router.get("/{id}/", response_model=KosaricaDB)
async def read_kosarica(id: int = Path(..., gt=0),):
    kosarica = await crud.get(id)
    if not kosarica:
        raise HTTPException(status_code=404, detail="Kosarica ni bila najdena")
    return kosarica



@router.put("/{id}/", response_model=KosaricaDB)
async def posodobi_kosarico(payload: KosaricaSchema, id: int = Path(..., gt=0),):
    kosarica = await crud.get(id)
    if not kosarica:
        raise HTTPException(status_code=404, detail="Kosarica ni bila najdena.")

    kosarica_id = await crud.put(id, payload)

    response_object = {
        "id": kosarica_id,
        "imeKosarice": payload.imeKosarice,
        "seznamTrgovin": payload.seznamTrgovin,
    }
    return response_object


@router.delete("/{id}/", response_model=KosaricaDB)
async def delete_kosarica(id: int = Path(..., gt=0)):
    kosarica = await crud.get(id)
    if not kosarica:
        raise HTTPException(status_code=404, detail="Kosarica ni bila najdena.")

    await crud.delete(id)

    return kosarica
'''