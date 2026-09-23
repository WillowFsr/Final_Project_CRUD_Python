from database.connection import Base
from sqlalchemy import Column, String, Integer,Numeric,Text
import sqlalchemy

class Produto(Base):
  __tablename__ = 'produto'

  id_prod = Column(Integer,autoincrement=True, primary_key=True)
  nome = Column(String, nullable=False)
  preco = Column(Numeric, nullable=False)
  descricao = Column(Text, nullable=False)
  estoque = Column(Integer,nullable=False)
