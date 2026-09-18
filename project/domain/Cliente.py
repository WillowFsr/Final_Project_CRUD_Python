from __future__ import annotations
from typing import Optional
from Usuario import Usuario
from Cartao import Cartao
from Carrinho import Carrinho
 

class Cliente(Usuario):
  def __init__(self, nome: str, idade:int , endereco:str, nacionalidade:str, id_usr: Optional[int] = None,):
    super().__init__(nome, idade, endereco, nacionalidade, id_usr)
    self.cartoes:list[Cartao] = []
  
  def inserir_cartao() -> None:
    pass
  
  def remover_cartao() -> bool:
    pass

  def listar_cartoes() -> None:
    pass
