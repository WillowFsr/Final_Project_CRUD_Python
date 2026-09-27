from __future__ import annotations
from typing import Optional
from project.infra.configs.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey


class Carrinho(Base):
  __tablename__ = "carrinho"

  id_carrinho: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
  id_cliente: Mapped[Optional[int]] = mapped_column(ForeignKey("cliente.id_cli"))
  cliente: Mapped["Cliente"] = relationship("Cliente", back_populates="carrinho")
  produtos_carrinho: Mapped[list["Produto_Carrinho"]] = relationship("Produto_Carrinho", back_populates="carrinho", cascade="all, delete-orphan")