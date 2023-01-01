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
