from sqlalchemy.orm import Session

from . import modelsDN, schemasDN

#get za kosarico z idjem 
async def get_kosarica(db: Session, kosarica_id: int):
    return db.query(modelsDN.Kosarica).filter(modelsDN.Kosarica.id == kosarica_id).first()

#get za vse kosarice
async def get_all_kosarice(db: Session, skip: int = 0, limit: int = 100):
    return db.query(modelsDN.Kosarica).offset(skip).limit(limit).all()

#tuki pomoje nared sam da makosarica prazn seznam izdelkov
#post za kosarico 
def create_kosarica(db: Session, kosarica: schemasDN.KosaricaCreate):
    db_kosarica = modelsDN.Kosarica(imeKosarice=kosarica.imeKosarice)
    db.add(db_kosarica)
    db.commit()
    db.refresh(db_kosarica)
    return db_kosarica


#stari ostanki
'''
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
'''