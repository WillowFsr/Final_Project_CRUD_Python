from project.api.schemas.Base import Base
from pydantic import ConfigDict, Field

# ProdutoCarrinho classes, needed on Carrinho class
class ProdutoCarrinhoBase(Base):
  id_prod:int = Field(ge=1)
  quantidade:int = Field(ge=1)
  

class ProdutoCarrinhoRequest(ProdutoCarrinhoBase):
  pass

class ProdutoCarrinhoResponse(ProdutoCarrinhoBase):
  model_config = ConfigDict(from_attributes=True)
  
  id_produto_carrinho:int = Field(ge=1)
  
  
#Carrinho classe
class CarrinhoBase(Base):
  pass

class CarrinhoResponse(CarrinhoBase):
  model_config = ConfigDict(from_attributes=True)
  
  id_cli:int = Field(ge=1)
  id_carrinho:int = Field(ge=1)
  
  produto_carrinho:list["ProdutoCarrinhoResponse"]



  
  