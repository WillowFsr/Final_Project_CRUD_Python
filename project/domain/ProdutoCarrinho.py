from __future__ import annotations
from Carrinho import Carrinho
from Produto import Produto

class ProdutoCarrinho:
  def __init__(self, produto:Produto,quantidade:int):
    self.produto = produto
    self.quantidade = quantidade
  
  def subtotal_produtos(self) -> float:
    return self.produto.preco * quantidade
