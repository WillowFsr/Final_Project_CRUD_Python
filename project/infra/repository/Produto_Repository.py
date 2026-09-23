from project.infra.configs.connection import DBConnectionHandler
from project.infra.entities.produto import Produto as Produto_Entity
from project.domain.Produto import Produto as Produto_Domain

class Produto_Repository:
  @staticmethod
  def to_tuple(produto_domain:Produto_Domain) -> tuple[str, float, str, int]:
    return (produto_domain.nome,produto_domain.preco,produto_domain.descricao,produto_domain.estoque)

  @staticmethod
  def from_db(produto_entity:Produto_Entity)-> Produto_Domain:
    if(not produto_entity):
      return None
    
    return Produto_Domain(
      id_prod=produto_entity.id_prod,
      nome=produto_entity.nome,
      preco=produto_entity.preco,
      descricao=produto_entity.descricao,
      estoque=produto_entity.estoque
    )

  def insert():
    pass
  