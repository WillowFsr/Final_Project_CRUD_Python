from project.infra.repository.Produto_Repository import Produto_Repository


class RemoverEstoque:

  def remover_estoque(self, id_prod: int, quantidade: int) -> bool:
    if (not isinstance(id_prod, int)):
      return False

    if (id_prod < 1):
      return False

    if (not isinstance(quantidade, int)):
      return False

    if (quantidade <= 0):
      return False

    produto = Produto_Repository().search(id_prod)

    if (not produto):
      return False

    try:
      produto.remover_estoque(quantidade)
    except (TypeError, ValueError):
      return False

    return Produto_Repository().update(id_prod,produto)