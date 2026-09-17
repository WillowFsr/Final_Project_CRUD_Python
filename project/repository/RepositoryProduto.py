from typing import Optional, List
from project.database import connection 
from project.domain.Produto import Produto

class RepositoryProduto:
  
  def create(self, produto:Produto) -> Produto:
    sql = "INSERT INTO produtos(nome, preco, descricao) VALUES (#%s,%s,%s ) RETURNING id_prod"
    with connection.iniciar_connexao() as conn:
      if conn:
        with conn.

  def list_one(self, id_produto: int)-> Optional[Produto]:
    pass

  def list_all(self) -> list[Produto]:
    pass

  def update(self)-> Produto:
    pass

  def delete(self) -> Produto:
    pass
