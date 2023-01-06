from typing import List
from fastapi import APIRouter, HTTPException, Path, Depends, FastAPI
from sqlalchemy.orm import Session
from .databaseDN import SessionLocal, engine, username, password, hostname, database

#za loging
import sentry_sdk
from sentry_sdk import set_level


#za metrike
from prometheus_fastapi_instrumentator import Instrumentator

#local import files
from app import crudDN, modelsDN, schemasDN

#za health and livnes info 
from fastapi_health import health
from datetime import datetime
import psycopg2

#za middleware
from fastapi.middleware.cors import CORSMiddleware

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

#------APP-INIT------
#inicializiraj app
app = FastAPI(
    title="Kosarice",
    description="Mikrostoritev, ki skrbi za kosarice izdelkov in \
        primerjavo cen teh izdelkov med različnimi trgovinami",
    root_path="/kosaricems",
    docs_url="/openapi",
)

#------MIDDLEWARE------
origins = [
    ""
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)

#------METRIKE------ 
# za metrike izpostavi /metrics
@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)

modelsDN.Base.metadata.create_all(bind=engine)


#------HEALTH and LIVNES------

#naredi dict za prikazat health in livenes checks
async def health_success_failure_handler(**conditions):
    rez = {"status": "UP", "checks": []}
    for cond in conditions:
        to_add = {
            "name": cond,
            "status": conditions[cond]
        }
        rez["checks"].append(to_add)
        if not conditions[cond]:
            rez["status"] = "DOWN"
    return rez

#pridobi stanje povezljivosti z bazo 
def check_db_connection():
    try:
        #se poskusi povezat na bazo
        conn = psycopg2.connect(f"dbname={database} user={username} host={hostname} password={password} "
                                f"connect_timeout=1")
        
        #zapre povezavo z bazo
        conn.close()
        
        #če si se povezal na bazo potem vrni True
        return True
    except:
        print("I am unable to connect to the database")
        return False


#pridobi stanje mikrostoritve
def get_ms_status():
    global broken
    return not broken

#Preveri ali je mikrostoritev živa
def is_ms_alive():
    if broken or not database_working:
        return False
    return True


#globalna spremenljivka za "pokvarit" storitev (for demo)
broken = False

#globalna spremenljivka za delovanje baze
database_working = True

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


#not sure kako točno tole dela odstranil en check(za prostor v bazi)
health_handler = health([get_ms_status, check_db_connection],
                        success_handler=health_success_failure_handler,
                        failure_handler=health_success_failure_handler)

#doda poti za health in liveness 
app.add_api_route("/health/liveness", health_handler, name="check liveness")
app.add_api_route("/health/readiness", health_handler, name="check readiness")


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
#TODO na fronendu se bo dodajal ta objekt i guess
@app.post("/kosarice/{kosarica_id}/izdelki/", response_model=schemasDN.Izdelek)
def create_izdelek_for_kosarica(kosarica_id: int, izdelek: schemasDN.IzdelekCreate, db: Session = Depends(get_db)):
    return crudDN.create_izdelek_kosarico(db=db, izdelek=izdelek, kosarica_id=kosarica_id)

