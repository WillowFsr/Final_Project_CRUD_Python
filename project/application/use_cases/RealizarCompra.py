from __future__ import annotations

from project.domain.Produto import Produto as Produto_Domain

from project.infra.repository.Cliente_Repository import Cliente_Repository as Cliente_Repo
from project.infra.repository.Cartao_Repository import Cartao_Repository as Cartao_Repo
from project.infra.repository.Carrinho_Repository import Carrinho_Repository as Carrinho_Repo

from project.application.use_cases.RemoverEstoque import RemoverEstoque
from project.application.use_cases.RemoverSaldo import RemoverSaldo


class RealizarCompra:

  @staticmethod
  def verificar_estoque(produto: Produto_Domain, quantidade_compra: int) -> bool:
    return produto.estoque >= quantidade_compra

  def realizar_compra(self, id_cliente: int, id_cartao: int) -> bool:
    if (not isinstance(id_cartao, int) or not isinstance(id_cliente, int)):
      return False

    if (id_cartao < 1 or id_cliente < 1):
      return False

    cliente_repo = Cliente_Repo()
    cartao_repo = Cartao_Repo()
    carrinho_repo = Carrinho_Repo()

    remover_estoque = RemoverEstoque()
    remover_saldo = RemoverSaldo()

    cliente = cliente_repo.search(id_cliente)

    if (not cliente):
      return False

    carrinho = carrinho_repo.search_by_cli(id_cliente)

    if (not carrinho):
      return False

    itens = carrinho.produto_no_carrinho()

    if (not itens):
      return False

    cartao = cartao_repo.search(id_cartao)

    if (not cartao):
      return False

    if (cartao.id_cli != id_cliente):
      return False

    valor_total = carrinho.calcular_total()

    if (cartao.saldo < valor_total):
      return False

    for item in itens:
      if (not self.verificar_estoque(item.produto, item.quantidade)):
        return False

    for item in itens:
      if (not remover_estoque.remover_estoque(
        item.produto.id_prod,
        item.quantidade
      )):
        return False

    if (not remover_saldo.remover_saldo(id_cartao, valor_total)):
      return False

    from project.infra.repository.Historico_Repository import Historico_Compra_Repository as Historico

    historico = Historico.registrar_compra(
      id_cliente,
      valor_total,
      itens
    )

    if (not historico):
      return False

    carrinho.limpar_carrinho()

    if (not carrinho_repo.update(carrinho)):
      return False

    return True