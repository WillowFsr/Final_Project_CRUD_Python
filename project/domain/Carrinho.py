from __future__ import annotations

from typing import Any, Optional
from decimal import Decimal

from project.domain.Produto import Produto
from project.domain.ProdutoCarrinho import ProdutoCarrinho


class Carrinho:

  def __init__(self, id_carrinho: Optional[int] = None, id_cli: Optional[int] = None):
    self.id_carrinho = id_carrinho
    self.id_cli = id_cli
    self._produto_carrinho: list[ProdutoCarrinho] = []

  def to_dict(self) -> dict[str, Any]:
    return {
      "itens": [item.to_dict() for item in self._produto_carrinho],
      "total": self.calcular_total()
    }

  def adicionar_produto(self, produto: Produto, quantidade: int) -> bool:
    if (not isinstance(produto, Produto)):
      raise TypeError("Informe um produto corretamente")

    if (not isinstance(quantidade, int)):
      raise TypeError("A quantidade de um produto deve ser inteiro")

    if (quantidade <= 0):
      raise ValueError("A quantidade deve ser maior que zero")

    novo_produto = ProdutoCarrinho(produto, quantidade)

    for produto_carrinho in self._produto_carrinho:
      if (novo_produto.produto.id_prod == produto_carrinho.produto.id_prod):
        produto_carrinho.quantidade += novo_produto.quantidade
        return True

    self._produto_carrinho.append(novo_produto)
    return True

  def remover_produto(self, produto: Produto) -> bool:
    if (not isinstance(produto, Produto)):
      raise TypeError("Informe um produto corretamente")

    for produto_carrinho in self._produto_carrinho:
      if (produto.id_prod == produto_carrinho.produto.id_prod):
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

  @property
  def id_carrinho(self) -> Optional[int]:
    return self._id_carrinho

  @id_carrinho.setter
  def id_carrinho(self, id_carrinho: Optional[int]) -> None:
    if (id_carrinho is not None and not isinstance(id_carrinho, int)):
      raise TypeError("A entrada deve ser um numero inteiro")

    self._id_carrinho = id_carrinho

  @property
  def id_cli(self) -> Optional[int]:
    return self._id_cli

  @id_cli.setter
  def id_cli(self, id_cli: Optional[int]) -> None:
    if (id_cli is not None and not isinstance(id_cli, int)):
      raise TypeError("A entrada deve ser um numero inteiro")

    self._id_cli = id_cli

  @property
  def produto_carrinho(self) -> list[ProdutoCarrinho]:
    return self._produto_carrinho.copy()

  @produto_carrinho.setter
  def produto_carrinho(self, produto_carrinho: list[ProdutoCarrinho]) -> None:
    if (not isinstance(produto_carrinho, list)):
      raise TypeError("A entrada deve ser uma lista")

    for item in produto_carrinho:
      if (not isinstance(item, ProdutoCarrinho)):
        raise TypeError("A lista deve conter apenas ProdutoCarrinho")

    self._produto_carrinho = produto_carrinho.copy()