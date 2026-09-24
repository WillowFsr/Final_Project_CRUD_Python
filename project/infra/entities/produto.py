from project.infra.configs.base import Base
from sqlalchemy import Column, String, Integer, Numeric, Text, SmallInteger
from sqlalchemy.orm import mapped_column, Mapped

class Produto(Base):
  __tablename__ = 'produto'

  id_prod:Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement= True, nullable= False)
  nome:Mapped[str] = mapped_column(String, nullable=False)
  preco:Mapped[float] = mapped_column(Numeric, nullable=False)
  descricao = mapped_column(Text, nullable=True)
  estoque = mapped_column(SmallInteger, nullable=False)
