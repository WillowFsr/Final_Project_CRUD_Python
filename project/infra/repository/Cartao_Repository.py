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

  def insert(self, cartao_domain:Cartao_Domain) -> bool:
    if (not isinstance(cartao_domain, Cartao_Domain)):
      return False
    
    with DBConnectionHandler() as db:
      cartao_entity = Cartao_Entity(numero= cartao_domain.numero, validade= cartao_domain.validade, cvv=cartao_domain.cvv, bandeira=cartao_domain.bandeira, saldo=cartao_domain.saldo)

      db.session.add(cartao_entity)
      return True
  
  def delete(self, id_cartao:int) -> bool:
    if (not isinstance(id_cartao, int)):
      return False
    if (id_cartao<1):
      return False
     
    with DBConnectionHandler() as db:
      cartao_delete = db.session.query(Cartao_Entity).filter_by(id_cartao=id_cartao).first()

      if not cartao_delete:
        return False
      
      db.session.delete(cartao_delete)
    
    return True

  def search(self, id_cartao:int) -> Cartao_Domain | None:
    if (not isinstance(id_cartao, int)):
      return None
    if (id_cartao<1):
      return None
    
    with DBConnectionHandler() as db:
      cartao_busca = db.session.query(Cartao_Entity).filter_by(id_cartao=id_cartao).first()

      return self.from_db(cartao_busca)
  
  def update(self, id_cartao:int, cartao_domain:Cartao_Domain) -> bool:
    if (not isinstance(cartao_domain,Cartao_Domain)):
      return False
    if (not isinstance(id_cartao, int)):
      return False
    if (id_cartao<1):
      return False
    
    with DBConnectionHandler() as db:
      cartao_entity = db.session.query(Cartao_Entity).filter_by(id_cartao=id_cartao).first()
      
      if not cartao_entity:
        return False
      
      cartao_entity.numero = cartao_domain.numero
      cartao_entity.validade = cartao_domain.validade
      cartao_entity.cvv = cartao_domain.cvv
      cartao_entity.bandeira = cartao_domain.bandeira
      cartao_entity.saldo = cartao_domain.saldo
      
    return True
