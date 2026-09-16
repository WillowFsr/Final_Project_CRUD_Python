from typing import Optional

class Produto:
  def __init__(self, produto_nome: str, produto_preco: float, produto_descricao:str,id_produto: Optional[int] = None ):
    self.produto_nome = produto_nome
    self.produto_preco = produto_preco
    self.produto_descricao = produto_descricao
    self.id_produto = id_produto
  
  def desconto(self,porcentagem_desconto:int |float) -> None:
    if (not isinstance(porcentagem_desconto,(int, float) )):
      raise TypeError(f"A entrada deve ser um número  ")
    if (porcentagem_desconto <0 ):
      raise ValueError(f"Valor do desconto não pode ser menor que 0")
    
    fator_desconto = 1 -(porcentagem_desconto/100)
    self.produto_preco = self.produto_preco * fator_desconto


  def aumento(self, porcentagem_aumento:int |float) -> None:
    if (not isinstance(porcentagem_aumento,(int,float))):
      raise TypeError(f"A entrada deve ser um número ")
    if (porcentagem_aumento <0 ):
      raise ValueError(f"Valor do aumento não pode ser 0 ou menos")
    
    fator_aumento = 1 + (porcentagem_aumento/100)
    self.produto_preco = self.produto_preco * fator_aumento
  
  def atualizar_descricao(self, nova_descricao:str) -> None:
    if(not isinstance(nova_descricao, str)):
      raise TypeError(f"A entrada deve ser um texto(string)")
    if(not nova_descricao.strip()):
      raise ValueError(f"Ao atualizar uma descrição, ela não pode continuar vazia")
    self.produto_descricao = nova_descricao
 
 
  #Getters
  @property
  def produto_nome(self) ->str:
    return self._produto_nome

  @property
  def produto_preco(self) -> float:
    return self._produto_preco
  
  @property
  def produto_descricao(self) -> str:
    return self._produto_descricao
  
  @property
  def id_produto(self) -> Optional[int]:
    return self._id_produto
  
  #Setters
  @produto_nome.setter
  def produto_nome(self, nome:str) -> None:
    if (not isinstance(nome,str)):
      raise TypeError(f"A entrada deveria ser um texto(string)")
    if (not nome.strip()):
      raise ValueError(f"O nome do produto não pode ser vazio")
      
    self._produto_nome = nome  

  @produto_preco.setter
  def produto_preco(self, preco: float) -> None:
    if(not isinstance(preco, (int,float))):
      raise TypeError(f"A entrada deveria ser um número(int ou float)")
    if (preco <0):
      raise ValueError(f"A entrada não pode ser negativa")
    
    self._produto_preco = preco
  
  @produto_descricao.setter
  def produto_descricao(self, descricao:str) -> None:
    if (not isinstance(descricao, str)):
      raise TypeError(f"A entrada deveria ser um texto(string)")
    
    self._produto_descricao = descricao
  
  @id_produto.setter
  def id_produto(self, id_prod: Optional[int]) -> None:
    if(id_prod is not None and not isinstance(id_prod,int)):
      raise TypeError("O ID do produto deverá ser um inteiro")
    self._id_produto = id_prod