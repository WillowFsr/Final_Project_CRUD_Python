from project.infra.configs.base import Base
from sqlalchemy import Column, String, Integer, Numeric, Text, SmallInteger

class Produto(Base):
  __tablename__ = 'produto'

  id_prod = Column(Integer,primary_key=True, autoincrement= True, nullable= False)
  nome = Column(String, nullable=False)
  preco = Column(Numeric, nullable=False)
  descricao = Column(Text, nullable=True)
  estoque = Column(SmallInteger, nullable=False)
