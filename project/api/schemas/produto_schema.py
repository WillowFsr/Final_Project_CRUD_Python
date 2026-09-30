from __future__ import annotations
from project.api.schemas.Base import Base
from pydantic import ConfigDict, Field
from decimal import Decimal

class ProdutoBase(Base):
  nome: str = Field(min_length=1, max_length=90)
  preco: Decimal = Field(ge=Decimal("0.00"))
  descricao: str | None = Field(default=None,min_length=1)
  estoque: int = Field(ge=0)
  
class ProdutoRequest(ProdutoBase):
  pass

class ProdutoResponse(ProdutoBase):
  model_config = ConfigDict(from_attributes=True)
  
  id_prod:int = Field(ge=1)
  

class EstoqueRequest(Base):
  estoque:int = Field(ge=0)
  