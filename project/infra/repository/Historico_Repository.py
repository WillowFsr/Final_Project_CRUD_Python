from decimal import Decimal
from project.infra.configs.connection import DBConnectionHandler
from project.infra.entities.historico_compra import Historico_Compra as Historico_Entity
from project.infra.entities.item_historico import Item_Historico_Compra as Item_Entity

class Historico_Compra_Repository:  # ou Historico_Compra_Infra
  
  @staticmethod
  def registrar_compra(id_cli: int, valor_total: Decimal, itens_carrinho: list) -> bool:
    """
    Salva o log da compra diretamente na infraestrutura, respeitando 
    exatamente o schema do banco e o nome da entidade.
    """
    with DBConnectionHandler() as db:
      # 1. Cria o registro principal na tabela 'historico_compra'
      historico_entity = Historico_Entity(
          id_cli=id_cli,
          valor_total=valor_total
      )
      
      # 2. Varre os itens do carrinho e preenche a tabela 'item_historico'
      for item_carrinho in itens_carrinho:
        produto = item_carrinho.produto
        
        item_entity = Item_Entity(
            id_prod=produto.id_prod,
            quantidade=item_carrinho.quantidade,
            preco_momento=produto.preco
        )
        historico_entity.itens.append(item_entity)
      
      # 3. Salva no banco de dados
      db.session.add(historico_entity)
      
    return True