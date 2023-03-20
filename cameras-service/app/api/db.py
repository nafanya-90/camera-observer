import os

from sqlalchemy import (Column, Integer, Boolean, MetaData, String, Table,
                        create_engine, ARRAY)

from databases import Database

DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
metadata = MetaData()

cameras = Table(
    'cameras',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('is_active', Boolean),
    Column('name', String(50)),
    Column('location', String(50)),
    Column('location_details', String(255)),
    Column('url', String(255)),
)

database = Database(DATABASE_URI)
