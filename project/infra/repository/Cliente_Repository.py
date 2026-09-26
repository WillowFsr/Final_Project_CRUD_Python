from __future__ import annotations
from typing import Optional
from project.infra.configs.connection import DBConnectionHandler
from project.domain.Cliente import Cliente as Cliente_Domain
from project.infra.entities.cliente import Cliente as Cliente_Entity

class Cliente_Repository:
  @staticmethod
  def to_tuple(cliente_domain:Cliente_Domain) -> tuple[str, int, str, str]:
    return (cliente_domain.nome, cliente_domain.idade, cliente_domain.endereco, cliente_domain.nacionalidade, cliente_domain.id_cli)

  @staticmethod
  def from_db(cliente_entity:Cliente_Entity) -> Cliente_Domain | None:
    if (not isinstance(cliente_entity, Cliente_Entity)):
      return None
    
    cliente = Cliente_Domain(nome= cliente_entity.nome, idade=cliente_entity.idade, endereco=cliente_entity.endereco,nacionalidade=cliente_entity.nacionalidade,id_cli=cliente_entity.id_cli )

    from project.infra.repository.Cartao_Repository import Cartao_Repository

    if hasattr(cliente_entity, 'cartoes') and isinstance(cliente_entity.cartoes,list):
      for cartao_entity in cliente_entity.cartoes:
        cartao_domain = Cartao_Repository.from_db(cartao_entity)
        if cartao_domain:
          cliente.inserir_cartao(cartao_domain)

    return cliente

  def insert(self, cliente_domain:Cliente_Domain) -> bool:
    if(not isinstance(cliente_domain, Cliente_Domain)):
      return False
    
    with DBConnectionHandler() as db:
      cliente_entity = Cliente_Entity(nome=cliente_domain.nome, idade=cliente_domain.idade, endereco=cliente_domain.endereco,nacionalidade= cliente_domain.nacionalidade)
      
      from project.infra.entities.cartao import Cartao as Cartao_Entity
      
      for cliente_cartao in cliente_domain.cartoes:
        cartao_entity = Cartao_Entity(numero=cliente_cartao.numero, validade=cliente_cartao.validade, cvv=cliente_cartao.cvv, bandeira=cliente_cartao.bandeira, saldo=cliente_cartao.saldo)
        cliente_entity.cartoes.append(cartao_entity)
      
      db.session.add(cliente_entity)
    
    return True
      
  def search(self, cli_id:int) -> Cliente_Domain | None:
    if(not isinstance(cli_id,int)):
      return None
    if(cli_id<1):
      return None

    with DBConnectionHandler() as db:
      cliente_busca = db.session.query(Cliente_Entity).filter_by(id_cli=cli_id).first()
      return self.from_db(cliente_busca)
  
  def delete(self, cli_id:int) -> bool:
    if (not isinstance(cli_id,int)):
      return False
    if (cli_id <1):
      return False
    
    with DBConnectionHandler() as db:
      cliente_entity = db.session.query(Cliente_Entity).filter_by(id_cli=cli_id).first()

      if not cliente_entity:
        return False
      
      db.session.delete(cliente_entity)
      return True
  
  def update(self, cli_id:int, cliente_domain:Cliente_Domain) -> bool:
    if (not isinstance(cliente_domain, Cliente_Domain)):
      return False
    if ( not isinstance(cli_id, int)):
      return False
    if (cli_id<1):
      return False
    
    with DBConnectionHandler() as db:
      cliente_entity = db.session.query(Cliente_Entity).filter_by(id_cli=cli_id).first()

      if not cliente_entity:
        return False
      
      cliente_entity.nome = cliente_domain.nome
      cliente_entity.idade = cliente_domain.idade
      cliente_entity.endereco = cliente_domain.endereco
      cliente_entity.nacionalidade = cliente_domain.nacionalidade

    return True

