from project.infra.configs.base import Base
from sqlalchemy import String, Integer, Numeric, Text, SmallInteger
from sqlalchemy.orm import mapped_column, Mapped
from decimal import Decimal
from typing import Optional

class Produto(Base):
  __tablename__ = 'produto'

  id_prod:Mapped[int] = mapped_column(primary_key=True, autoincrement= True)
  nome:Mapped[str] = mapped_column()
  preco:Mapped[Decimal] = mapped_column(Numeric)
  descricao:Mapped[Optional[str]] = mapped_column(nullable=True)
  estoque:Mapped[int] = mapped_column(default=0)
