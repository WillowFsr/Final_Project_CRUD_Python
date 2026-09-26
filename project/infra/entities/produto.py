from __future__ import annotations
from project.infra.configs.base import Base
from sqlalchemy import String, Integer, Numeric, Text, SmallInteger
from sqlalchemy.orm import mapped_column, Mapped, relationship
from decimal import Decimal
from typing import Optional

class Produto(Base):
  __tablename__ = 'produto'

  id_prod:Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement= True)
  nome:Mapped[str] = mapped_column(String, nullable=False)
  preco:Mapped[Decimal] = mapped_column(Numeric, nullable=False)
  descricao:Mapped[Optional[str]] = mapped_column(Text, nullable=True)
  estoque:Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)

  item_historico:Mapped[list["Item_Historico_Compra"]] = relationship("Item_Historico_Compra", back_populates="produto")  