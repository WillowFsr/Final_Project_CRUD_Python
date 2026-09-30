from __future__ import annotations

from project.infra.configs.connection import DBConnectionHandler

from project.domain.Carrinho import Carrinho as Carrinho_Domain
from project.domain.ProdutoCarrinho import ProdutoCarrinho

from project.infra.entities.carrinho import Carrinho as Carrinho_Entity
from project.infra.entities.produto import Produto as Produto_Entity
from project.infra.entities.produto_carrinho import Produto_Carrinho as Produto_Carrinho_Entity

from project.infra.repository.Produto_Repository import Produto_Repository as Prod_Repo


class Carrinho_Repository:

  @staticmethod
  def from_db(carrinho_entity: Carrinho_Entity) -> Carrinho_Domain | None:
    if (not isinstance(carrinho_entity, Carrinho_Entity)):
      return None

    carrinho = Carrinho_Domain(carrinho_entity.id_carrinho,carrinho_entity.id_cli)

    produtos_carrinho = []

    for item in carrinho_entity.produto_carrinho:
      produto = Prod_Repo.from_db(item.produto)

      if (not produto):
        return None

      produto_carrinho = ProdutoCarrinho(produto,item.quantidade,item.id_produto_carrinho,item.id_carrinho)

      produtos_carrinho.append(produto_carrinho)

    carrinho.produto_carrinho = produtos_carrinho

    return carrinho

  def insert(self, carrinho_domain: Carrinho_Domain) -> bool:
    if (not isinstance(carrinho_domain, Carrinho_Domain)):
      return False
    if (not isinstance(carrinho_domain.id_cli, int)):
      return False
    if (carrinho_domain.id_cli < 1):
      return False

    with DBConnectionHandler() as db:
      produtos_entity = []

      for item in carrinho_domain.produto_no_carrinho():
        produto_entity = db.session.query(Produto_Entity).filter_by(
          id_prod=item.produto.id_prod
        ).first()

        if (not produto_entity):
          return False

        produtos_entity.append((item, produto_entity))

      carrinho_entity = Carrinho_Entity(id_cli=carrinho_domain.id_cli)

      db.session.add(carrinho_entity)
      db.session.flush()

      carrinho_domain.id_carrinho = carrinho_entity.id_carrinho

      itens_entity = []

      for item, produto_entity in produtos_entity:
        produto_carrinho_entity = Produto_Carrinho_Entity(
          carrinho=carrinho_entity,
          produto=produto_entity,
          quantidade=item.quantidade
        )

        db.session.add(produto_carrinho_entity)
        itens_entity.append((item, produto_carrinho_entity))

      db.session.flush()

      for item, item_entity in itens_entity:
        item.id_produto_carrinho = item_entity.id_produto_carrinho
        item.id_carrinho = item_entity.id_carrinho

      return True

  def search(self, id_carrinho: int) -> Carrinho_Domain | None:
    if (not isinstance(id_carrinho, int)):
      return None

    if (id_carrinho < 1):
      return None

    with DBConnectionHandler() as db:
      carrinho_entity = db.session.query(Carrinho_Entity).filter_by(
        id_carrinho=id_carrinho
      ).first()

      if (not carrinho_entity):
        return None

      return self.from_db(carrinho_entity)

  def delete(self, id_carrinho: int) -> bool:
    if (not isinstance(id_carrinho, int)):
      return False

    if (id_carrinho < 1):
      return False

    with DBConnectionHandler() as db:
      carrinho_entity = db.session.query(Carrinho_Entity).filter_by(
        id_carrinho=id_carrinho
      ).first()

      if (not carrinho_entity):
        return False

      db.session.delete(carrinho_entity)

      return True
    
  def update(self, carrinho_domain: Carrinho_Domain) -> bool:
    if (not isinstance(carrinho_domain, Carrinho_Domain)):
      return False
    if (not isinstance(carrinho_domain.id_carrinho, int)):
      return False
    if (carrinho_domain.id_carrinho < 1):
      return False
    if (not isinstance(carrinho_domain.id_cli, int)):
      return False
    if (carrinho_domain.id_cli < 1):
      return False

    with DBConnectionHandler() as db:
      carrinho_entity = db.session.query(Carrinho_Entity).filter_by(
        id_carrinho=carrinho_domain.id_carrinho
      ).first()

      if (not carrinho_entity):
        return False

      produtos_entity = []

      for item in carrinho_domain.produto_no_carrinho():
        produto_entity = db.session.query(Produto_Entity).filter_by(
          id_prod=item.produto.id_prod
        ).first()

        if (not produto_entity):
          return False

        produtos_entity.append((item, produto_entity))

      carrinho_entity.id_cli = carrinho_domain.id_cli

      for item in list(carrinho_entity.produto_carrinho):
        db.session.delete(item)

      db.session.flush()

      itens_entity = []

      for item, produto_entity in produtos_entity:
        produto_carrinho_entity = Produto_Carrinho_Entity(
          carrinho=carrinho_entity,
          produto=produto_entity,
          quantidade=item.quantidade
        )

        db.session.add(produto_carrinho_entity)
        itens_entity.append((item, produto_carrinho_entity))

      db.session.flush()

      for item, item_entity in itens_entity:
        item.id_produto_carrinho = item_entity.id_produto_carrinho
        item.id_carrinho = item_entity.id_carrinho

      return True