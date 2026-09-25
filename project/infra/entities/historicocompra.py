  from __future__ import annotations
  from project.infra.configs.base import Base
  from sqlalchemy.orm import func, Mapped, mapped_column, relationship
  from sqlalchemy import DateTime, Integer, ForeignKey, Numeric
  from datetime import datetime
  from decimal import Decimal

  class Historico_Compra(Base):
    __tablename__ = 'historico_compra'

    id_historico:Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True, unique=True)
    id_cli:Mapped[int] = mapped_column(ForeignKey("cliente.id_cli"), nullable=False)

    valor_total:Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    data_compra:Mapped[datetime] = mapped_column(DateTime, nullable=False, insert_default=func.now())

    cliente:Mapped["Cliente"] = relationship("Cliente", back_populates='historico_compras')

    itens:Mapped[list["Item_Historico_Compra"]] = relationship("Item_Historico_Compra", back_populates="historico", cascade='all,delete-orphan')

