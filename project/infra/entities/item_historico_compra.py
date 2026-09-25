from __future__ import annotations
from infra.configs.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, Numeric
from decimal import Decimal

class Item_Historico_Compra(Base):
  __tablename__ = 'item_historico'

  id_item:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
  id_historico:Mapped[int] = mapped_column(ForeignKey('historico_compra.id_historico'), nullable=False)
  id_prod:Mapped[int] = mapped_column(ForeignKey('produto.id_prod'), nullable=False)

  quantidade:Mapped[int] = mapped_column(Integer, nullable=False)
  preco_momento: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

  historico:Mapped["Historico_Compra"] = relationship("Historico_Compra", back_populates="itens")
  produto:Mapped["Produto"] = relationship("Produto",back_populates="item_historico")