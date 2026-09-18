from __future__ import annotations
from Cliente import Cliente
from Cartao import Cartao

class ProcessadorPagamento:
  @staticmethod
  def processarcompra(cliente:Cliente, carrinho:Carrinho, cartao:Cartao) -> bool:
    return True