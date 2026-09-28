from __future__ import annotations

import os
import sys
from decimal import Decimal
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.orm import configure_mappers

PROJECT_DIR = Path(__file__).resolve().parent
ROOT = PROJECT_DIR.parent

if str(ROOT) not in sys.path:
  sys.path.insert(0, str(ROOT))

load_dotenv(ROOT / ".env")

if str(ROOT) not in sys.path:
  sys.path.insert(0, str(ROOT))

load_dotenv(ROOT / ".env")

REQUIRED_VARS = (
  "DB_HOST",
  "DB_PORT",
  "DB_NAME",
  "DB_USER",
  "DB_PASSWORD"
)

EXPECTED_TABLES = {
  "cliente",
  "cartao",
  "produto",
  "carrinho",
  "produto_carrinho",
  "historico_compra",
  "item_historico"
}


def titulo(texto: str) -> None:
  print("\n" + "=" * 72)
  print(texto)
  print("=" * 72)


def validar_configuracao() -> None:
  faltando = [variavel for variavel in REQUIRED_VARS if not os.getenv(variavel)]

  if faltando:
    raise RuntimeError("Variáveis ausentes no .env: " + ", ".join(faltando))


def validar_banco() -> None:
  from project.infra.configs.connection import DBConnectionHandler

  with DBConnectionHandler() as db:
    banco, usuario, schema = db.session.execute(
      text("SELECT current_database(), current_user, current_schema()")
    ).one()

    tabelas = set(db.session.execute(text("""
      SELECT table_name
      FROM information_schema.tables
      WHERE table_schema = 'public'
    """)).scalars().all())

  faltando = EXPECTED_TABLES - tabelas

  if faltando:
    raise RuntimeError("Tabelas ausentes no PostgreSQL: " + ", ".join(sorted(faltando)))

  print(f"Banco: {banco}")
  print(f"Usuário: {usuario}")
  print(f"Schema: {schema}")
  print("[OK] As 7 tabelas esperadas existem.")


def listar_clientes() -> None:
  from project.infra.configs.connection import DBConnectionHandler
  from project.infra.entities.cliente import Cliente as Cliente_Entity

  with DBConnectionHandler() as db:
    clientes = db.session.query(Cliente_Entity).order_by(
      Cliente_Entity.id_cli
    ).all()

    clientes_info = [
      (cliente.id_cli, cliente.nome)
      for cliente in clientes
    ]

  print("\nClientes existentes no banco:")

  if not clientes_info:
    print("Nenhum cliente encontrado.")
    return

  for id_cli, nome in clientes_info:
    print(f"  ID {id_cli} | {nome}")


def ler_id(mensagem: str) -> int:
  while True:
    try:
      valor = int(input(mensagem).strip())

      if valor < 1:
        raise ValueError

      return valor
    except ValueError:
      print("Informe um ID inteiro maior que zero.")


def exibir_carrinho(cliente) -> Decimal:
  carrinho = cliente.carrinho

  print(f"\nCliente: {cliente.nome} (id={cliente.id_cli})")

  if not carrinho:
    raise RuntimeError("Este cliente não possui carrinho.")

  itens = carrinho.produto_no_carrinho()

  if not itens:
    raise RuntimeError("O carrinho deste cliente está vazio. Nenhuma compra será realizada.")

  print(f"Carrinho: {carrinho.id_carrinho}")
  print("Itens:")

  for item in itens:
    subtotal = item.subtotal_produtos()
    print(
      f"  - {item.produto.nome} | "
      f"qtd={item.quantidade} | "
      f"preço={item.produto.preco} | "
      f"subtotal={subtotal} | "
      f"estoque={item.produto.estoque}"
    )

  total = carrinho.calcular_total()
  print(f"Total da compra: R$ {total:.2f}")
  return total


def exibir_cartoes(cliente) -> None:
  print("\nCartões do cliente:")

  if not cliente.cartoes:
    raise RuntimeError("Este cliente não possui cartão cadastrado.")

  for cartao in cliente.cartoes:
    numero = str(cartao.numero)
    mascarado = "*" * max(0, len(numero) - 4) + numero[-4:]
    print(
      f"  ID {cartao.id_cartao} | "
      f"bandeira={cartao.bandeira} | "
      f"número={mascarado} | "
      f"saldo=R$ {cartao.saldo:.2f}"
    )


def listar_historico(id_cliente: int) -> None:
  from project.infra.repository.Historico_Repository import Historico_Compra_Repository
  from project.infra.repository.Produto_Repository import Produto_Repository

  historicos = Historico_Compra_Repository.listar_por_cliente(id_cliente)

  titulo("HISTÓRICO DE COMPRAS DO CLIENTE")

  if not historicos:
    print("Nenhuma compra encontrada para este cliente.")
    return

  produto_repo = Produto_Repository()

  for numero, historico in enumerate(historicos, start=1):
    print(f"Compra {numero}")
    print(f"  ID histórico: {historico['id_historico']}")
    print(f"  Data: {historico['data_compra']}")
    print(f"  Total: R$ {Decimal(historico['valor_total']):.2f}")
    print("  Itens:")

    for item in historico["itens"]:
      produto = produto_repo.search(item["id_prod"])
      nome_produto = produto.nome if produto else f"Produto #{item['id_prod']}"
      preco = Decimal(item["preco_momento"])
      quantidade = item["quantidade"]
      subtotal = preco * quantidade

      print(
        f"    - {nome_produto} | "
        f"qtd={quantidade} | "
        f"preço no momento=R$ {preco:.2f} | "
        f"subtotal=R$ {subtotal:.2f}"
      )

    print()


def executar_compra() -> None:
  from project.application.use_cases.RealizarCompra import RealizarCompra
  from project.infra.repository.Cliente_Repository import Cliente_Repository

  cliente_repo = Cliente_Repository()

  listar_clientes()
  id_cliente = ler_id("\nDigite o ID do cliente que fará a compra: ")

  cliente = cliente_repo.search(id_cliente)

  if not cliente:
    raise RuntimeError("Cliente não encontrado.")

  total = exibir_carrinho(cliente)
  exibir_cartoes(cliente)

  id_cartao = ler_id("Digite o ID do cartão que será usado: ")

  cartao_escolhido = next(
    (cartao for cartao in cliente.cartoes if cartao.id_cartao == id_cartao),
    None
  )

  if not cartao_escolhido:
    raise RuntimeError("O cartão informado não pertence a este cliente.")

  if cartao_escolhido.saldo < total:
    raise RuntimeError("O cartão selecionado não possui saldo suficiente.")

  print("\nA operação abaixo é uma COMPRA REAL no banco de dados.")
  print(f"Cliente: {cliente.nome}")
  print(f"Total: R$ {total:.2f}")
  print(f"Cartão: {id_cartao}")

  confirmacao = input("Confirmar compra? [s/N]: ").strip().lower()

  if confirmacao != "s":
    print("Compra cancelada. Nenhuma alteração foi feita pelo use case.")
    return

  resultado = RealizarCompra().realizar_compra(id_cliente, id_cartao)

  if not resultado:
    raise RuntimeError("O use case informou que a compra não foi realizada.")

  print("\n[OK] Compra realizada com sucesso.")

  cliente_depois = cliente_repo.search(id_cliente)

  if not cliente_depois:
    raise RuntimeError("Não foi possível reler o cliente após a compra.")

  titulo("ESTADO APÓS A COMPRA")

  cartao_depois = next(
    (cartao for cartao in cliente_depois.cartoes if cartao.id_cartao == id_cartao),
    None
  )

  if cartao_depois:
    print(f"Saldo do cartão após a compra: R$ {cartao_depois.saldo:.2f}")

  itens_depois = cliente_depois.carrinho.produto_no_carrinho() if cliente_depois.carrinho else []
  print(f"Itens restantes no carrinho: {len(itens_depois)}")

  listar_historico(id_cliente)


def main() -> int:
  titulo("COMPRA REAL - USE CASE RealizarCompra")

  try:
    validar_configuracao()

    from project.infra import entities
    configure_mappers()
    print("[OK] Mappers configurados.")

    validar_banco()
    executar_compra()

    return 0

  except Exception as exc:
    print("\n[ERRO]")
    print(f"Tipo: {type(exc).__name__}")
    print(f"Detalhe: {exc}")
    return 1


if __name__ == "__main__":
  raise SystemExit(main())
