from typing import Optional

class Produto:
  def __init__(self, nome: str, preco: float, descricao:str,id_prod: Optional[int] = None ):
    self.nome = nome
    self.preco = preco
    self.descricao = descricao
    self.id_prod = id_prod
  
  # - > Methods
  
  #used on json and api routes
  def to_dict(self)-> dict[str,any]:
    return{
      "id": self.id_prod,
      "nome": self.nome,
      "preco": self.preco,
      "descricao": self.descricao 
    }
  
  #used on connection in database on commands like insert and update
  def to_tuple(self) -> tuple(str, float, str):
    return (self.nome, self.preco,self.descricao)

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
  
  def atualizar_descricao(self, nova_descricao:str) -> None:
    if(not isinstance(nova_descricao, str)):
      raise TypeError(f"A entrada deve ser um texto(string)")
    if(not nova_descricao.strip()):
      raise ValueError(f"Ao atualizar uma descrição, ela não pode continuar vazia")
    self.descricao = nova_descricao
 
 
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
      raise TypeError("O ID do produto deverá ser um inteiro")
    self._id_prod = id_prod