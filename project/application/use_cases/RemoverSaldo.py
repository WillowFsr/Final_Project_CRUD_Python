from decimal import Decimal

from project.infra.repository.Cartao_Repository import Cartao_Repository


class RemoverSaldo:

  def remover_saldo(self, id_cartao: int, valor: Decimal) -> bool:
    if (not isinstance(id_cartao, int)):
      return False

    if (id_cartao < 1):
      return False

    if (not isinstance(valor, Decimal)):
      return False

    if (valor <= 0):
      return False

    cartao = Cartao_Repository().search(id_cartao)

    if (not cartao):
      return False

    try:
      cartao.remover_saldo(valor)
    except (TypeError, ValueError):
      return False

    return Cartao_Repository().update(cartao)