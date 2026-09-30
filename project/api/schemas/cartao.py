from project.api.schemas.Base import Base
from pydantic import ConfigDict, Field

from datetime import date
from decimal import Decimal

def validade_padrao() -> date:
  hoje = date.today()
  return hoje.replace(year=hoje.year+5)

class CartaoBase(Base):
  numero:str = Field(min_length=16, max_length=16)
  validade:date = Field(default_factory=validade_padrao)
  cvv:str = Field(min_length=3,max_length=3)
  bandeira:str = Field(min_length=1, max_length=20)

class CartaoRequest(CartaoBase):
  pass

class CartaoResponse(CartaoBase):
  model_config = ConfigDict(from_attributes=True)
  
  id_cartao:int = Field(ge=1)
  id_cli:int = Field(ge=1)
  saldo:Decimal = Field(ge=Decimal("0.00"))