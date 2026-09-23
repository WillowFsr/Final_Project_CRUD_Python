from __future__ import annotations
from typing import Any, Optional
from Produto import Produto
from project.domain.ProdutoCarrinho import ProdutoCarrinho

class Carrinho:
  def __init__(self):
    self._produto_carrinho:list[ProdutoCarrinho] = []
  
  def to_dict(self) -> dict[str, Any]:
    return {
      "itens": [item.to_dict() for item in self._produto_carrinho],
      "total": self.calcular_total()
      }

  def adicionar_produto(self, produto:Produto, quantidade:int) -> bool:
    if (not isinstance(produto, Produto)):
      raise TypeError(f"Informe um produto corretamente")
    if(not isinstance(quantidade, int)):
      raise TypeError(f"A quantidade de um produto deve ser inteiro")
    if(quantidade <=0):
      raise ValueError(f"Para adicionar uma quantidade de um produto em um carrinho, deve ser maior que zero")
    
    novo_produto:ProdutoCarrinho = ProdutoCarrinho(produto,quantidade)
    for produtocarrinho in self._produto_carrinho:
      if(novo_produto.produto == produtocarrinho.produto):
        produtocarrinho.quantidade += novo_produto.quantidade
        return True
    
    self._produto_carrinho.append(novo_produto)
    return True

  def remover_produto(self, produto:Produto,) -> bool:
    if (not isinstance(produto, Produto)):
      raise TypeError(f"Informe um produto de corretamente")
    
    for produtocarrinho in self._produto_carrinho:
      if(produto == produtocarrinho.produto):
        self._produto_carrinho.remove(produtocarrinho)
        return True
    
    raise ValueError(f"Produto nao encontrado")

  def produto_no_carrinho(self) -> list[ProdutoCarrinho]:
    return self._produto_carrinho.copy()
  
  def limpar_carrinho(self) -> None:
    self._produto_carrinho.clear()
  
  def calcular_total(self) -> float:
    valor_total:float = 0.0
    for produtocarrinho in self._produto_carrinho:
      valor_total += produtocarrinho.subtotal_produtos()
    return valor_total
