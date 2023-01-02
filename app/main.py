from typing import List
from fastapi import APIRouter, HTTPException, Path, Depends, FastAPI
from sqlalchemy.orm import Session
from databaseDN import SessionLocal, engine

#za loging
import sentry_sdk
from sentry_sdk import set_level

#za metrike
from prometheus_fastapi_instrumentator import Instrumentator

#local import files
import crudDN, modelsDN, schemasDN

#za health and livnes info 
from fastapi_health import health
from datetime import datetime

#------LOGGING------
# enable logging on Sentry
sentry_sdk.init(
    dsn="https://60d860690425432bb80de5af728ffe3b@o4504418811641857.ingest.sentry.io/4504418813280256",
    traces_sample_rate=1.0,
    debug=False,
)
set_level("info")

#------DATE-TIME------
#date and time za izpise 
def get_date_and_time():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


#inicializiraj app
app = FastAPI()

#------METRIKE------ 
# za metrike izpostavi /metrics
@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)

modelsDN.Base.metadata.create_all(bind=engine)


#------HEALTH and LIVNES------

#pridobi stanje mikrostoritve
def get_ms_status():
    if broken:
        return {"status": "The microservice is BROKEN", 
                "date": get_date_and_time()}
    return {"status": "The microservice is working",
            "date": get_date_and_time()}


#Preveri ali je mikrostoritev živa
def is_ms_alive():
    if broken:
        return False
    return True

#dodaj pot do preverjanja health in livness
app.add_api_route("/health/liveness", health([is_ms_alive, get_ms_status]))

#globalna spremenljivka za "pokvarit" storitev (for demo)
broken = False

#"pokvari" mikrostoritev
@app.post("/break")
async def break_app():
    global broken
    broken = True
    return {"The ms has been broken"}

#"popravi" mikrostoritev
@app.post("/unbreak")
async def unbreak_app():
    global broken 
    broken = False
    return {"The ms is fixed"}

#------ CORE funkcionalnosti ------

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#pridobi vse košarice v bazi
@app.get("/kosarice", response_model=List[schemasDN.Kosarica])
async def read_all_kosarice(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crudDN.get_all_kosarice(db, skip=skip, limit=limit)


#ustavri novo košarico če ne obstaja neka košarica z istim imenom
@app.post("/kosarice/", response_model=schemasDN.Kosarica)
async def create_kosarica(kosarica: schemasDN.KosaricaCreate, db: Session = Depends(get_db)):
    db_kosarica = crudDN.get_kosarica(db, imeKosarice=kosarica.imeKosarice)
    #print(db_kosarica.imeKosarice)
    if db_kosarica:
        raise HTTPException(status_code=400, detail="Kosarica ze obstaja")
    return crudDN.create_kosarica(db=db, kosarica=kosarica)


#za testiranje samo vrača kar dobi
@app.get("/kosarice/{id}")
async def get_kosarica(id: int):
    return f"This is the id that was sent through {id}."


#košarici s podanim id-jem dodaj nek izdelek
#TODO posodobi, da bo izdelek dodan iz podatkov iz Timotove MS (to na frontendu al tuki?)
@app.post("/kosarice/{kosarica_id}/izdelki/", response_model=schemasDN.Izdelek)
def create_izdelek_for_kosarica(kosarica_id: int, izdelek: schemasDN.IzdelekCreate, db: Session = Depends(get_db)):
    return crudDN.create_izdelek_kosarico(db=db, izdelek=izdelek, kosarica_id=kosarica_id)

