from __future__ import annotations
from infra.configs.base import Base
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Cliente(Base):
  __tablename__ = 'cliente'

  id_cli:Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True, unique=True)
  nome:Mapped[str] = mapped_column(String, nullable=False)
  idade:Mapped[int] = mapped_column(Integer, nullable=False)
  endereco:Mapped[str] = mapped_column(String, nullable=False)
  nacionalidade:Mapped[str] = mapped_column(String, nullable=False)

  cartoes:Mapped[list["Cartao"]] = relationship("Cartao",back_populates="cliente")
  historico_compras:Mapped[list["Historico_Compra"]] = relationship("Historico_Compra", back_populates="cliente" , cascade='all, delete-orphan')