from __future__ import annotations
from typing import Any, Optional
from decimal import Decimal
from project.domain.Produto import Produto
from project.domain.ProdutoCarrinho import ProdutoCarrinho


class Carrinho:

  def __init__(self, id_carrinho: Optional[int] = None, id_cliente: Optional[int] = None):
    self.id_carrinho = id_carrinho
    self.id_cliente = id_cliente
    self._produto_carrinho: list[ProdutoCarrinho] = []

  def to_dict(self) -> dict[str, Any]:
    return {
      "itens": [item.to_dict() for item in self._produto_carrinho],
      "total": self.calcular_total()
    }

  def adicionar_produto(self, produto: Produto, quantidade: int) -> bool:
    if not isinstance(produto, Produto):
      raise TypeError("Informe um produto corretamente")

    if not isinstance(quantidade, int):
      raise TypeError("A quantidade de um produto deve ser inteiro")

    if quantidade <= 0:
      raise ValueError("A quantidade deve ser maior que zero")

    novo_produto = ProdutoCarrinho(produto, quantidade)

    for produto_carrinho in self._produto_carrinho:
      if novo_produto.produto == produto_carrinho.produto:
        produto_carrinho.quantidade += novo_produto.quantidade
        return True

    self._produto_carrinho.append(novo_produto)
    return True

  def remover_produto(self, produto: Produto) -> bool:
    if not isinstance(produto, Produto):
      raise TypeError("Informe um produto corretamente")

    for produto_carrinho in self._produto_carrinho:
      if produto == produto_carrinho.produto:
        self._produto_carrinho.remove(produto_carrinho)
        return True

    raise ValueError("Produto nao encontrado")

  def produto_no_carrinho(self) -> list[ProdutoCarrinho]:
    return self._produto_carrinho.copy()

  def limpar_carrinho(self) -> None:
    self._produto_carrinho.clear()

  def calcular_total(self) -> Decimal:
    valor_total = Decimal("0.00")

    for produto_carrinho in self._produto_carrinho:
      valor_total += produto_carrinho.subtotal_produtos()

    return valor_total