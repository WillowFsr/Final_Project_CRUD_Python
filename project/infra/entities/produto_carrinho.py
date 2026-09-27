from __future__ import annotations
from project.infra.configs.base import Base
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Produto_Carrinho(Base):
  __tablename__ = "produto_carrinho"

  id_produto_carrinho: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,unique=True)

  id_carrinho: Mapped[int] = mapped_column(ForeignKey("carrinho.id_carrinho"),nullable=False)

  id_prod: Mapped[int] = mapped_column(ForeignKey("produto.id_prod"),nullable=False)

  quantidade: Mapped[int] = mapped_column(Integer,nullable=False)
  carrinho: Mapped["Carrinho"] = relationship("Carrinho",back_populates="produtos_carrinho")

  produto: Mapped["Produto"] = relationship("Produto",back_populates="produto_carrinho")