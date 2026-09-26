from __future__ import annotations
from typing import Optional, Any
from project.domain.Usuario import Usuario
from project.domain.Cartao import Cartao
from project.domain.Carrinho import Carrinho
 
class Cliente(Usuario):
  def __init__(self, nome: str, idade:int , endereco:str, nacionalidade:str, id_cli: Optional[int] = None):
    super().__init__(nome, idade, endereco, nacionalidade)
    self.id_cli = id_cli
    self.cartoes:list[Cartao] = []
    self.carrinho:Carrinho = Carrinho()
  
  # - > Methods
  def to_dict(self) -> dict[str, Any]:
    dados = super().to_dict()
    dados["id_cli"] = self.id_cli
    dados["cartoes"] = [cartao.to_dict() for cartao in self.cartoes]
    dados["carrinho"] = self.carrinho.to_dict() if hasattr(self.carrinho, "to_dict") else []
    return dados  
  
  def inserir_cartao(self, cartao:Cartao) -> None:
    if(not isinstance(cartao, Cartao)):
      raise TypeError(f"Para inserir um cartao ao cliente, coloque um objeto cartao válido")
    if(cartao in self.cartoes):
      raise ValueError(f"Cartao já inserido")
    
    if(self.id_cli is not None):
      cartao.id_cli = self.id_cli
    
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

  # Getter e Setter para id_cli
  @property
  def id_cli(self) -> Optional[int]:
    return self._id_cli

  @id_cli.setter
  def id_cli(self, id_cli: Optional[int]) -> None:
    if(id_cli is not None and not isinstance(id_cli, int)):
      raise TypeError("O ID do cliente deverá ser um inteiro")
    self._id_cli = id_cli