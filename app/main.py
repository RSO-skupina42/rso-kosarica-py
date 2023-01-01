from typing import List

from fastapi import APIRouter, HTTPException, Path, Depends, FastAPI
from sqlalchemy.orm import Session

#za loging
import sentry_sdk
from sentry_sdk import set_level

#local import files
import crudDN, modelsDN, schemasDN

from databaseDN import SessionLocal, engine

# enable logging
sentry_sdk.init(
    dsn="https://60d860690425432bb80de5af728ffe3b@o4504418811641857.ingest.sentry.io/4504418813280256",
    traces_sample_rate=1.0,
    debug=True,
)
set_level("info")


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
@app.get("/kosarice", response_model=List[schemasDN.Kosarica])
async def read_all_kosarice(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crudDN.get_all_kosarice(db, skip=skip, limit=limit)


#ustavri novo košarico
@app.post("/kosarice/", response_model=schemasDN.Kosarica)
async def create_kosarica(kosarica: schemasDN.KosaricaCreate, db: Session = Depends(get_db)):
    db_kosarica = crudDN.get_kosarica(db, imeKosarice=kosarica.imeKosarice)
    #print(db_kosarica.imeKosarice)
    if db_kosarica:
        raise HTTPException(status_code=400, detail="Kosarica ze obstaja")
    return crudDN.create_kosarica(db=db, kosarica=kosarica)


#za testiranje 
@app.get("/kosarice/{id}")
async def get_kosarica(id: int):
    return f"This is the id that was sent through {id}."

@app.post("/kosarice/{kosarica_id}/izdelki/", response_model=schemasDN.Izdelek)
def create_izdelek_for_kosarica(kosarica_id: int, izdelek: schemasDN.IzdelekCreate, db: Session = Depends(get_db)):
    return crudDN.create_izdelek_kosarico(db=db, izdelek=izdelek, kosarica_id=kosarica_id)

