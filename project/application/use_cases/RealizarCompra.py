from __future__ import annotations
from typing import Optional, Any
from decimal import Decimal

#domain importations
from project.domain.Cliente import Cliente as Cliente_Domain
from project.domain.Produto import Produto as Produto_Domain

#repository importations
from project.infra.repository.Cliente_Repository import Cliente_Repository as Cliente_Repo
from project.infra.repository.Produto_Repository import Produto_Repository as Produto_Repo


class RealizarCompra:
  
  def realizar_compra(self, id_cliente:int, id_cartao:int) -> bool:
    if (not isinstance(id_cartao, int) or not isinstance(id_cliente, int)):
      return False
    if (id_cartao<1 or id_cliente<1):
      return False
    
    cliente = Cliente_Repo().search(id_cliente)
    
    if not cliente:
      return False
    
    
  