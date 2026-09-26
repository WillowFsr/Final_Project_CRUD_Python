from __future__ import annotations
from project.infra.configs.connection import DBConnectionHandler
from project.infra.entities.produto import Produto as Produto_Entity
from project.domain.Produto import Produto as Produto_Domain
from typing import Optional

class Produto_Repository:
  @staticmethod
  def to_tuple(produto_domain:Produto_Domain) -> tuple[str, float, str, int]:
    return (produto_domain.nome,produto_domain.preco,produto_domain.descricao,produto_domain.estoque)

  @staticmethod
  def from_db(produto_entity: Produto_Entity) -> Produto_Domain | None:
    if not produto_entity:
      return None
      
    return Produto_Domain(id_prod=produto_entity.id_prod, nome=produto_entity.nome, preco=produto_entity.preco, descricao=produto_entity.descricao,  estoque=produto_entity.estoque)

  def insert(self, produto:Produto_Domain) -> bool:
    if (not isinstance(produto, Produto_Domain)):
      return False
    
    with DBConnectionHandler() as db:
      produto_entity = Produto_Entity(nome = produto.nome,preco= produto.preco, descricao= produto.descricao, estoque=produto.estoque)
      db.session.add(produto_entity)
      return True

  def delete(self, produto_id:int) -> bool:
    if(not isinstance(produto_id, int)):
      return False
    if(produto_id<1):
      return False
    
    with DBConnectionHandler() as db:
      produto_entity = db.session.query(Produto_Entity).filter_by(id_prod=produto_id).first()

      if not produto_entity:
        return False
      
      db.session.delete(produto_entity)
    
    return True

  def search(self, produto_id:int) -> Produto_Domain | None:
    if (not isinstance(produto_id, int)):
      return None
    if (produto_id<1):
      return None
    
    with DBConnectionHandler() as db:
      produto_entity_busca = db.session.query(Produto_Entity).filter_by(id_prod=produto_id).first()

      return self.from_db(produto_entity_busca)

  def update(self, produto_id:int, produto:Produto_Domain) -> bool:
    if (not isinstance(produto, Produto_Domain)):
      return False
    if (not isinstance(produto_id, int)):
      return False
    if (produto_id<1):
      return False
    
    with DBConnectionHandler() as db:
      produto_update = db.session.query(Produto_Entity).filter_by(id_prod=produto_id).first()

      if (not produto_update):
        return False
      
      produto_update.nome = produto.nome
      produto_update.preco = produto.preco
      produto_update.descricao = produto.descricao
      produto_update.estoque = produto.estoque

      return True
