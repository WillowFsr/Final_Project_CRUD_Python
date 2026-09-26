from __future__ import annotations
from decimal import Decimal
from typing import Optional
from project.domain.Cliente import Cliente
from project.domain.Cartao import Cartao
from project.domain.Carrinho import Carrinho
from project.domain.Produto import Produto

class ProcessadorPagamento:
  @staticmethod
  def processarcompra(cliente:Cliente, id_cartao: int) -> None:
    #binding cliente carrinho to a variable to facilitate logic and readability
    carrinho = cliente.carrinho
    
    #verifications
    if (not carrinho._produto_carrinho):
      raise ValueError(f"O carrinho está vazio")
    if(not isinstance(id_cartao,int)):
      raise TypeError(f"O id do cartao deve ser um numero inteiro")
    if(id_cartao<1):
      raise ValueError(f"O id do cartao nao pode ser menor ou igual a zero")

    #finding Cliente Cartao
    cliente_cartao:Optional[Cartao] = None
    for cartao in cliente.cartoes:
      if (cartao.numero == id_cartao):
        cliente_cartao = cartao
        break
    
    #returning error if not finding one
    if (cliente_cartao is None):
      raise ValueError(f"Catao nao encontrado")

    total_compra:Decimal = carrinho.calcular_total()

    if(total_compra > cliente_cartao.saldo):
      raise ValueError(f"Saldo insuficiente para a compra")
    
    cliente_cartao.saldo -= total_compra

    #changing Produto.quantidade to deduce stock
    for produto_carrinho in carrinho._produto_carrinho:
      produto = produto_carrinho._produto
      quantidade_comprada = produto_carrinho.quantidade

      if (quantidade_comprada > produto.estoque):
        raise ValueError(f"Estoque insuficiente para o produto {produto.nome}")
      
      produto.estoque -= quantidade_comprada
    
    carrinho.limpar_carrinho()