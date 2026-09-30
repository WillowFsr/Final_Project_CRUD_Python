from __future__ import annotations
from project.infra.configs.base import Base
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Carrinho(Base):
  __tablename__ = "carrinho"

  id_carrinho: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,unique=True)

  id_cli: Mapped[int] = mapped_column(ForeignKey("cliente.id_cli"),nullable=False,unique=True)

  cliente: Mapped["Cliente"] = relationship("Cliente",back_populates="carrinho")

  produto_carrinho: Mapped[list["Produto_Carrinho"]] = relationship("Produto_Carrinho",back_populates="carrinho",cascade="all, delete-orphan")