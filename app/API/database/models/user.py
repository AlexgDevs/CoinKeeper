from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ...database import Base

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(255))
    balance: Mapped[int] = mapped_column(default=0)

    categories: Mapped[List['Category']] = relationship('Category', back_populates='user')
    transactions: Mapped[List['Transaction']] = relationship('Transaction', back_populates='user')