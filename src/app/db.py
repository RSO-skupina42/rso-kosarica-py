import os

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    create_engine
)

'''from sqlalchemy.dialects.postgresql import ARRAY

from sqlalchemy.orm import relationship
'''
from sqlalchemy.sql import func

from databases import Database

'''from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()'''

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

#table za kosarice
kosarice = Table(
    "kosarice",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("imeKosarice", String(50)),

    #tuki more met nekak seznam ne string za seznamtrgovin
    Column("seznamTrgovin", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

'''
class Kosarice(Base):  
    __tablename__= 'kosarice'
    id = Column(Integer, nullable=False, primary_key=True)
    imeKosarice = Column(String,nullable=False)
    seznamTrgovin = Column(ARRAY(String),nullable=False)
    '''


# databases query builder
database = Database(DATABASE_URL)
