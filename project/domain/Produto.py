from __future__ import annotations #it serves to from db method
from typing import Optional, Any
from decimal import Decimal

class Produto:
  def __init__(self, nome: str, preco: Decimal, descricao:str, estoque:int, id_prod: Optional[int] = None ):
    self.id_prod = id_prod
    self.nome = nome
    self.preco = preco
    self.descricao = descricao
    self.estoque = estoque
  
  # - > Methods
  
  #used on json and api routes, just in case of future updates
  def to_dict(self)-> dict[str,Any]:
    return{
      "id": self.id_prod,
      "nome": self.nome,
      "preco": self.preco,
      "estoque": self.estoque,
      "descricao": self.descricao 
    } 

  def desconto(self,porcentagem_desconto:int |float) -> None:
    if (not isinstance(porcentagem_desconto,(int, float) )):
      raise TypeError(f"A entrada deve ser um número  ")
    if (porcentagem_desconto <0 ):
      raise ValueError(f"Valor do desconto não pode ser menor que 0")
    
    fator_desconto = 1 -(porcentagem_desconto/100)
    self.preco = self.preco * fator_desconto

  def aumento(self, porcentagem_aumento:int |float) -> None:
    if (not isinstance(porcentagem_aumento,(int,float))):
      raise TypeError(f"A entrada deve ser um número ")
    if (porcentagem_aumento <0 ):
      raise ValueError(f"Valor do aumento não pode ser 0 ou menos")
    
    fator_aumento = 1 + (porcentagem_aumento/100)
    self.preco = self.preco * fator_aumento
 

  #Getters
  @property
  def nome(self) ->str:
    return self._nome

  @property
  def preco(self) -> Decimal:
    return self._preco
  
  @property
  def descricao(self) -> str:
    return self._descricao
  
  @property
  def id_prod(self) -> Optional[int]:
    return self._id_prod
  
  @property
  def estoque(self) -> int:
    return self._estoque
  #Setters
  @nome.setter
  def nome(self, nome:str) -> None:
    if (not isinstance(nome,str)):
      raise TypeError(f"A entrada deveria ser um texto(string)")
    if (not nome.strip()):
      raise ValueError(f"O nome do produto não pode ser vazio")
      
    self._nome = nome  

  @preco.setter
  def preco(self, preco: Decimal) -> None:
    if(not isinstance(preco, Decimal)):
      raise TypeError(f"A entrada deveria ser um número")
    if (preco <0):
      raise ValueError(f"A entrada não pode ser negativa")
    
    self._preco = preco
  
  @descricao.setter
  def descricao(self, descricao:str) -> None:
    if (not isinstance(descricao, str)):
      raise TypeError(f"A entrada deveria ser um texto(string)")
    
    self._descricao = descricao
  
  @id_prod.setter
  def id_prod(self, id_prod: Optional[int]) -> None:
    if(id_prod is not None and not isinstance(id_prod,int)):
      raise TypeError(f"O ID do produto deverá ser um inteiro")
    self._id_prod = id_prod
  
  @estoque.setter
  def estoque(self, estoque:int|float) -> None:
    if( not isinstance(estoque, (float,int))):
      raise TypeError(f"O estoque de um produto tem que ser um numero")
    if (estoque <0):
      raise ValueError(f"O estoque tem que ser maior ou igual a zero")
    self._estoque = int(estoque)