from __future__ import annotations
from typing import Optional
from Usuario import Usuario
from Cartao import Cartao
from Carrinho import Carrinho
 

class Cliente(Usuario):
  def __init__(self, nome: str, idade:int , endereco:str, nacionalidade:str, id_usr: Optional[int] = None):
    super().__init__(nome, idade, endereco, nacionalidade, id_usr)
    self.cartoes:list[Cartao] = []
    self.carrinho:Carrinho = Carrinho()
  
  # - > Methods
  def to_dict(self) -> dict[str, Any]:
    dados = super().to_dict()
    dados["cartoes"] = [cartao.to_dict() for cartao in self.cartoes]
    dados["carrinho"] = self.carrinho.to_dict() if hasattr(self.carrinho, "to_dict") else []
    return dados

  def to_tuple(self) -> tuple[str, int, str, str]:
    return (self.nome, self.idade, self.endereco, self.nacionalidade)

  @staticmethod
  def from_db(linha: tuple) -> Cliente:
    return Cliente( id_usr=linha[0], nome=linha[1], idade=linha[2], endereco=linha[3], nacionalidade=linha[4])    
  
  def inserir_cartao(self, cartao:Cartao) -> None:
    if(not isinstance(cartao, Cartao)):
      raise TypeError(f"Para inserir um cartao ao cliente, coloque um objeto cartao válido")
    if(cartao in self.cartoes):
      raise ValueError(f"Cartao já inserido")
    #associate the cartao.id_user as the actual user. if a new client, mantain as none for the database associate the forgein key
    if(self.id_usr is not None):
      cartao.id_usr = self.id_usr
    
    self.cartoes.append(cartao)
    
  def remover_cartao(self, cartao:Cartao) -> bool:
    if(not isinstance(cartao,Cartao)):
      raise TypeError(f"Insira um cartao real")
    if(cartao in self.cartoes):
      self.cartoes.remove(cartao)
      return True
    return False

  def listar_cartoes(self) -> list[Cartao]:
    return self.cartoes.copy()
