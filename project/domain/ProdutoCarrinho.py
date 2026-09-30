from __future__ import annotations
from typing import Any, Optional
from decimal import Decimal
from project.domain.Produto import Produto

class ProdutoCarrinho:

  def __init__(self, produto: Produto, quantidade: int, id_produto_carrinho: Optional[int] = None, id_carrinho: Optional[int] = None):
    if (not isinstance(produto, Produto)):
      raise TypeError("A entrada não é um produto valido")
    self.id_produto_carrinho = id_produto_carrinho
    self.id_carrinho = id_carrinho
    self.produto = produto
    self.quantidade = quantidade

  def to_dict(self) -> dict[str, Any]:
    return {
      "id_produto_carrinho": self.id_produto_carrinho,
      "id_carrinho": self.id_carrinho,
      "id_prod": self.produto.id_prod,
      "produto": self.produto.to_dict(),
      "quantidade": self.quantidade,
      "subtotal": self.subtotal_produtos()
    }

  def subtotal_produtos(self) -> Decimal:
    return self.produto.preco * self.quantidade

  @property
  def id_produto_carrinho(self) -> Optional[int]:
    return self._id_produto_carrinho

  @id_produto_carrinho.setter
  def id_produto_carrinho(self, id_produto_carrinho: Optional[int]) -> None:
    if (id_produto_carrinho is not None and not isinstance(id_produto_carrinho, int)):
''      raise TypeError("A entrada deve ser um numero inteiro")
    self._id_produto_carrinho = id_produto_carrinho

  @property
  def id_carrinho(self) -> Optional[int]:
    return self._id_carrinho

  @id_carrinho.setter
  def id_carrinho(self, id_carrinho: Optional[int]) -> None:
    if (id_carrinho is not None and not isinstance(id_carrinho, int)):
      raise TypeError("A entrada deve ser um numero inteiro")
    self._id_carrinho = id_carrinho

  @property
  def produto(self) -> Produto:
    return self._produto

  @produto.setter
  def produto(self, produto: Produto) -> None:
    if (not isinstance(produto, Produto)):
      raise TypeError("A entrada não é um produto valido")
    self._produto = produto

  @property
  def id_prod(self) -> int:
    return self.produto.id_prod

  @property
  def quantidade(self) -> int:
    return self._quantidade

  @quantidade.setter
  def quantidade(self, quantidade: int) -> None:
    if (not isinstance(quantidade, int)):
      raise TypeError("A quantidade deve ser um numero inteiro")
    if (quantidade <= 0):
      raise ValueError("A quantidade de compra nao pode ser inferior ou igual a 0")
    if (quantidade > self.produto.estoque):
      raise ValueError("A quantidade de compra e superior ao estoque")
    self._quantidade = quantidade