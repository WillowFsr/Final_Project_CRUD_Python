from infra.configs.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Numeric, ForeignKey
from typing import Optional
from decimal import Decimal

class Cartao(Base):
  __tablename__ = 'cartao'

  id_cartao:Mapped[int] = mapped_column(primary_key=True, autoincrement=True,)
  id_cli
  numero:Mapped[int] = mapped_column(Integer, nullable=False)
  validade:Mapped[str]
  cvv:
  bandeira
  saldo