from typing import Literal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ...database import Base

class Transaction(Base):
    __tablename__ = 'transactions'
    id: Mapped[int] = mapped_column(primary_key=True)

    type: Mapped[Literal['Income', 'Expenditure']]
    amount: Mapped[int]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    user: Mapped['User'] = relationship('User', back_populates='transactions')
    category: Mapped['Category'] = relationship('Category', back_populates='transactions')