from __future__ import annotations
from typing import Any, Optional
from Produto import Produto
from ProdutoCarrinho import ProdutoCarrinho

class Carrinho:
  def __init__(self):
    self._produto_carrinho:list[ProdutoCarrinho] = []
  
  def adicionar_produto(self, produto:Produto):
    pass

  def remover_produto(self, produto:Produto, id_produto:Optional[int] = None):
    if (not isinstance(produto, Produto)):
      raise TypeError(f"Informe um produto de corretamente")
    if(not isinstance(id_produto, int)):
      raise TypeError(f"O id do produto é inválido")
    if(id_produto is not None and produto.id_prod == id_produto):
      self._produto_carrinho.remove(produto)
    else:
      if (produto in self._produto_carrinho):
        self._produto_carrinho.remove(produto)
      else:
        raise ValueError(f"Objeto não encontrado")

  