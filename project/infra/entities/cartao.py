from __future__ import annotations
from infra.configs.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Numeric, ForeignKey, Date, func
from typing import Optional
from decimal import Decimal
from datetime import date

class Cartao(Base):
  __tablename__ = 'cartao'

  id_cartao:Mapped[int] = mapped_column(primary_key=True, autoincrement=True,)
  id_cli:Mapped[int] = mapped_column(ForeignKey('cliente.id_cli'))
  numero:Mapped[int] = mapped_column(Integer, nullable=False)
  validade:Mapped[date] = mapped_column(Date, nullable=False, insert_default=func.current_date())
  cvv:Mapped[str] = mapped_column(String, nullable=False)
  bandeira:Mapped[str] = mapped_column(String, nullable=False)
  saldo:Mapped[Decimal] = mapped_column(Numeric,nullable=False, default=Decimal('0.00')) 

  cliente:Mapped[Optional["Cliente"]] = relationship()