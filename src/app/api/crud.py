from app.api.models import KosaricaSchema
from app.db import kosarice, database


async def post(payload: KosaricaSchema):
    query = kosarice.insert().values(imeKosarice=payload.imeKosarice, seznamTrgovin=payload.seznamTrgovin)
    return await database.execute(query=query)


async def get(id: int):
    query = kosarice.select().where(id == kosarice.c.id)
    return await database.fetch_one(query=query)


async def get_all():
    query = kosarice.select()
    return await database.fetch_all(query=query)


async def put(id: int, payload: KosaricaSchema):
    query = (
        kosarice
        .update()
        .where(id == kosarice.c.id)
        .values(imeKosarice=payload.imeKosarice, seznamTrgovin=payload.seznamTrgovin)
        .returning(kosarice.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = kosarice.delete().where(id == kosarice.c.id)
    return await database.execute(query=query)
