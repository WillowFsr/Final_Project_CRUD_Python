from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from project.infra.configs.base import Base
from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Historico_Compra(Base):
  __tablename__ = "historico_compra"

  id_historico: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,)

  id_cli: Mapped[int] = mapped_column(ForeignKey("cliente.id_cli",ondelete="CASCADE",),nullable=False,)

  valor_total: Mapped[Decimal] = mapped_column(Numeric(10, 2),nullable=False,)

  data_compra: Mapped[datetime] = mapped_column(DateTime,nullable=False,server_default=func.now(),)

  cliente: Mapped["Cliente"] = relationship("Cliente",back_populates="historico_compras",)

  itens: Mapped[list["Item_Historico_Compra"]] = relationship("Item_Historico_Compra",back_populates="historico",cascade="all, delete-orphan",)