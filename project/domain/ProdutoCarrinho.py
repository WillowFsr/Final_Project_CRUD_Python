from Produto import Produto
from typing import Any

class ProdutoCarrinho:
  def __init__(self, produto:Produto,quantidade:int):
    if (not isinstance(produto, Produto)):
      raise TypeError(f"A entrada não é um produto valido")
    self._produto = produto
    self.quantidade = quantidade
  
  def to_dict(self) -> dict[str, Any]:
    return {
      "produto": self._produto.to_dict(),
      "quantidade": self._quantidade,
      "subtotal": self.subtotal_produtos()
        }
  
  def subtotal_produtos(self) -> float:
    return self._produto.preco * self._quantidade

  @property
  def produto(self) -> Produto:
    return self._produto

  @property
  def quantidade(self) -> int:        
    return self._quantidade

  @quantidade.setter
  def quantidade(self, quantidade: int) -> None:
    if(not isinstance(quantidade, int)):
      raise TypeError(f"A quantidade deve ser um numero inteiro")
    if (quantidade <= 0):
      raise ValueError(f"A quantidade de compra nao pode ser inferior ou igual a 0")
    if(quantidade > self.produto.estoque):
      raise ValueError(f"A quantidade de compra e superior ao estoque")
    self._quantidade = quantidade