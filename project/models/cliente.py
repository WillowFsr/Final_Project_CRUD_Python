from database.connection import  Base
from sqlalchemy import Column,String, Integer, ForeignKey
import sqlalchemy

class cliente(Base) :
  __tablename__ = 'cliente'

  id_cli = Column(Integer,primary_key=True, autoincrement=True)
  nome = Column(String,nullable=False)
  idade = Column(Integer, nullable=False)
  endereco = Column(String,nullable=False)
  nacionalidade = Column(String,nullable=False)
