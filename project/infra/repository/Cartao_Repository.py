from __future__ import annotations
from typing import Optional
from decimal import Decimal
from datetime import date
from project.domain.Cartao import Cartao as Cartao_Domain
from project.infra.entities.cartao import Cartao as Cartao_Entity
from project.infra.configs.connection import DBConnectionHandler

class Cartao_Repository:
  @staticmethod
  def to_tuple(cartao_domain:Cartao_Domain) -> tuple[str, date, str, str, Decimal, Optional[int]]:
    return (cartao_domain.numero, cartao_domain.validade, cartao_domain.cvv, cartao_domain.bandeira, cartao_domain.saldo, cartao_domain.id_cli)

  @staticmethod
  def from_db(cartao_entity:Cartao_Entity) -> Cartao_Domain | None:
    if (not isinstance(cartao_entity, Cartao_Entity)):
      return None

    return Cartao_Domain(numero=cartao_entity.numero,validade=cartao_entity.validade,cvv=cartao_entity.cvv,bandeira=cartao_entity.bandeira,saldo=cartao_entity.saldo,id_cli=cartao_entity.id_cli,id_cartao=cartao_entity.id_cartao)