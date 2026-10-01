from decimal import Decimal

from project.infra.repository.Cartao_Repository import Cartao_Repository


class AdicionarSaldo:

  def adicionar_saldo(self, id_cartao: int, valor: Decimal) -> bool:
    cartao = Cartao_Repository().search(id_cartao)

    if (not cartao):
      return False

    try:
      cartao.adicionar_saldo(valor)
    except (TypeError, ValueError):
      return False
  
    return Cartao_Repository().update(id_cartao,cartao)