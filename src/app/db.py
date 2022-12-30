import os

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    ARRAY,
    create_engine
)

from sqlalchemy.sql import func

from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()
kosarice = Table(
    "kosarice",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("imeKosarice", String(50)),
    #tuki more met nekak seznam ne string za seznamtrgovin
    Column("seznamTrgovin", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)


# databases query builder
database = Database(DATABASE_URL)
