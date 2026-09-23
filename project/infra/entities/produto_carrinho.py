from sqlalchemy import Column,ForeignKey, Integer
from database.connection import Base

class Produto_Carrinho(Base):
  __tablename__ = 'produto_carrinho'

  id_prod = Column(Integer, nullable=False)
  quantidade = Column(Integer, nullable=False)
  
