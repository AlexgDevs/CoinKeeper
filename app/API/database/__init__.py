from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine(
    url='sqlite:///new.db',
    echo=True
)

Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass 

def up():
    Base.metadata.create_all(engine)

def drop():
    Base.metadata.drop_all(engine)

def migrate():
    drop()
    up()

from .models import (
    Category,
    User,
    Transaction
)