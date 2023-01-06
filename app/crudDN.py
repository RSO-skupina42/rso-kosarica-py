from sqlalchemy.orm import Session

from app import modelsDN

from app import schemasDN

#get za kosarico z idjem
def get_kosarica(db: Session, imeKosarice: str):
    return db.query(modelsDN.Kosarica).filter(modelsDN.Kosarica.imeKosarice == imeKosarice).first()

#get za vse kosarice
def get_all_kosarice(db: Session, skip: int = 0, limit: int = 100):
    return db.query(modelsDN.Kosarica).offset(skip).limit(limit).all()

#tuki pomoje nared sam da makosarica prazn seznam izdelkov
#post za kosarico
def create_kosarica(db: Session, kosarica: schemasDN.KosaricaCreate):
    db_kosarica = modelsDN.Kosarica(imeKosarice=kosarica.imeKosarice, ) # tuki morjo bit še osatli atributi? 
    db.add(db_kosarica)
    db.commit()
    db.refresh(db_kosarica)
    return db_kosarica

#funkcija za update kosarice 
def update_kosarica(db: Session, kosarica_id: int, kosarica: schemasDN.KosaricaUpdate):
    db_kosarica = db.query(modelsDN.Kosarica).filter(modelsDN.Kosarica.id == kosarica_id).first()
    db_kosarica.imeKosarice = db_kosarica.imeKosarice if db_kosarica.imeKosarice == "" else db_kosarica.imeKosarice
    db_kosarica.izdelki = kosarica.izdelki
    # db_user.foreign_key_cart = user.foreign_key_cart
    db.commit()
    db.refresh(db_kosarica)
    return db_kosarica

#naredi izdelek za kosarico 
def create_izdelek_kosarico(db: Session, izdelek: schemasDN.IzdelekCreate, kosarica_id: int):
    db_izdelk = modelsDN.Izdelek(**izdelek.dict(), kosarica_id=kosarica_id)
    db.add(db_izdelk)
    db.commit()
    db.refresh(db_izdelk)
    return db_izdelk
