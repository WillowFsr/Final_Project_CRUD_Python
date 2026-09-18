from __future__ import annotations #it serves to from db method
from typing import Optional, Any

class Produto:
  def __init__(self, nome: str, preco: float, descricao:str,quantidade:int,id_prod: Optional[int] = None ):
    self.id_prod = id_prod
    self.nome = nome
    self.preco = preco
    self.descricao = descricao
    self.quantidade = quantidade
  
  # - > Methods
  
  #used on json and api routes, just in case of future updates
  def to_dict(self)-> dict[str,Any]:
    return{
      "id": self.id_prod,
      "nome": self.nome,
      "preco": self.preco,
      "quantidade": self.quantidade,
      "descricao": self.descricao 
    }
  
  #used on connection in database on commands like insert and update, it could be unsderstandable of a way to transfer a class for a database
  def to_tuple(self) -> tuple[str, float, str,int] :
    return (self.nome, self.preco,self.descricao,self.quantidade)

  #its the oposite way, it transfer the data from database and turns it in to a object. it gets a tuple from database and sends it to the init method so it could be used to execute methods in the class
  @staticmethod
  def from_db(linha:tuple)-> Produto:
    return Produto(id_prod=linha[0], nome=linha[1], preco=linha[2], descricao=linha[3], quantidade=linha[4] )

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
  def preco(self) -> float:
    return self._preco
  
  @property
  def descricao(self) -> str:
    return self._descricao
  
  @property
  def id_prod(self) -> Optional[int]:
    return self._id_prod
  
  @property
  def quantidade(self) -> int:
    return self._quantidade
  #Setters
  @nome.setter
  def nome(self, nome:str) -> None:
    if (not isinstance(nome,str)):
      raise TypeError(f"A entrada deveria ser um texto(string)")
    if (not nome.strip()):
      raise ValueError(f"O nome do produto não pode ser vazio")
      
    self._nome = nome  

  @preco.setter
  def preco(self, preco: float) -> None:
    if(not isinstance(preco, (int,float))):
      raise TypeError(f"A entrada deveria ser um número(int ou float)")
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
  
  @quantidade.setter
  def quantidade(self, quantidade:int|float) -> None:
    if( not isinstance(quantidade, (float,int))):
      raise TypeError(f"A quantidade de um produto tem que ser um numero")
    if (quantidade<0):
      raise ValueError(f"A quantidade tem que ser maior que zero")
    self._quantidade = int(quantidade)