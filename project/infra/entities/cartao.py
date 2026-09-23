from sqlalchemy import Column, BigInteger, String, Numeric, Integer, ForeignKeyConstraint
from database.connection import Base

class Cartao(Base):
  __tablename__ = 'cartao'

  id_cartao = Column(Integer,autoincrement=True, nullable=False)
  id_cl = Colum(Integer, nullable=False)
  numero = Column(BigInteger, nullable=False)
  validade = Column(String,nullable=False)
  cvv = Column(String, nullable=False)
  bandeira = Column(String, nullable=False)
  valor = Column(Numeric, nullable=False)

