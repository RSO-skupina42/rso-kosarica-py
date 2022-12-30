from fastapi import FastAPI

from app.api import kosarica, ping
from app.db import database, engine, metadata

metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(ping.router)
app.include_router(kosarica.router, prefix="/kosarica", tags=["kosarice"])
