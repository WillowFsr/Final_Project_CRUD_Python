from __future__ import annotations
from project.infra.configs.connection import DBConnectionHandler
from project.domain.Carrinho import Carrinho as Carrinho_Domain
from project.infra.entities.carrinho  import Carrinho as Carrinho_Entity


class Carrinho_Repository:
  @staticmethod
  def from_db(carrinho_entity:Carrinho_Entity) -> Carrinho_Domain | None:
    if (not isinstance(carrinho_entity, Carrinho_Entity)):
      return None
    
    