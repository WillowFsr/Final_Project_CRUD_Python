from __future__ import annotations

import os
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.orm import configure_mappers


PROJECT_ROOT = Path(__file__).resolve().parent
ROOT = PROJECT_ROOT.parent

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
    raise RuntimeError(
      "Variáveis ausentes no .env: " + ", ".join(faltando)
    )


def testar_mappers() -> None:
  from project.infra import entities
  configure_mappers()
  print("[OK] Entities importadas e relationships configuradas.")


def testar_banco() -> None:
  from project.infra.configs.connection import DBConnectionHandler

  with DBConnectionHandler() as db:
    banco, usuario, schema = db.session.execute(
      text("SELECT current_database(), current_user, current_schema()")
    ).one()

    tabelas = set(
      db.session.execute(
        text("""
          SELECT table_name
          FROM information_schema.tables
          WHERE table_schema = 'public'
        """)
      ).scalars().all()
    )

  faltando = EXPECTED_TABLES - tabelas

  if faltando:
    raise RuntimeError(
      "Tabelas ausentes no PostgreSQL: " + ", ".join(sorted(faltando))
    )

  print(f"[OK] Banco: {banco}")
  print(f"[OK] Usuário: {usuario}")
  print(f"[OK] Schema: {schema}")
  print("[OK] As 7 tabelas esperadas existem.")


def salvar_dados() -> tuple[int, int, int]:
  from project.domain.Cartao import Cartao
  from project.domain.Cliente import Cliente
  from project.domain.Produto import Produto

  from project.infra.repository.Cartao_Repository import Cartao_Repository
  from project.infra.repository.Cliente_Repository import Cliente_Repository
  from project.infra.repository.Carrinho_Repository import Carrinho_Repository
  from project.infra.repository.Historico_Repository import Historico_Compra_Repository
  from project.infra.repository.Produto_Repository import Produto_Repository

  cliente_repo = Cliente_Repository()
  cartao_repo = Cartao_Repository()
  produto_repo = Produto_Repository()
  carrinho_repo = Carrinho_Repository()

  cliente = Cliente(
    nome="TESTE FINAL MAIN",
    idade=25,
    endereco="Rua de Teste, 123",
    nacionalidade="Brasileira"
  )

  cartao = Cartao(
    numero="TESTE-FINAL-0001",
    validade=date(2030, 12, 31),
    cvv="999",
    bandeira="TESTE",
    saldo=Decimal("1000.00")
  )

  cliente.inserir_cartao(cartao)

  if not cliente_repo.insert(cliente):
    raise RuntimeError("Falha ao inserir cliente e cartão.")

  print(f"[OK] Cliente persistido: id_cli={cliente.id_cli}")
  print(f"[OK] Cartão persistido: id_cartao={cartao.id_cartao}")

  produto = Produto(
    nome="PRODUTO TESTE FINAL",
    preco=Decimal("100.00"),
    descricao="Produto criado pelo main de integração.",
    estoque=10
  )

  if not produto_repo.insert(produto):
    raise RuntimeError("Falha ao inserir produto.")

  print(f"[OK] Produto persistido: id_prod={produto.id_prod}")

  cliente.carrinho.id_cliente = cliente.id_cli
  cliente.carrinho.adicionar_produto(produto, 2)

  if not carrinho_repo.insert(cliente.carrinho):
    raise RuntimeError("Falha ao inserir carrinho.")

  print(f"[OK] Carrinho persistido: id_carrinho={cliente.carrinho.id_carrinho}")
  print("[OK] Produto_Carrinho persistido através do Carrinho_Repository.")

  total = cliente.carrinho.calcular_total()
  itens = cliente.carrinho.produto_no_carrinho()

  if not Historico_Compra_Repository.registrar_compra(
    cliente.id_cli,
    total,
    itens
  ):
    raise RuntimeError("Falha ao inserir histórico de compra.")

  historicos = Historico_Compra_Repository.listar_por_cliente(cliente.id_cli)

  if not historicos:
    raise RuntimeError("Histórico não foi encontrado após o INSERT.")

  historico = historicos[0]

  print(f"[OK] Historico_Compra persistido: id_historico={historico['id_historico']}")
  print(f"[OK] Item_Historico persistido: {len(historico['itens'])} item(ns)")

  cliente_db = cliente_repo.search(cliente.id_cli)
  produto_db = produto_repo.search(produto.id_prod)
  cartao_db = cartao_repo.search(cartao.id_cartao)
  carrinho_db = carrinho_repo.search(cliente.carrinho.id_carrinho)

  if not cliente_db:
    raise RuntimeError("Cliente não pôde ser lido novamente.")

  if not produto_db:
    raise RuntimeError("Produto não pôde ser lido novamente.")

  if not cartao_db:
    raise RuntimeError("Cartão não pôde ser lido novamente.")

  if not carrinho_db:
    raise RuntimeError("Carrinho não pôde ser lido novamente.")

  if carrinho_db.id_cliente != cliente.id_cli:
    raise RuntimeError("Carrinho retornou com cliente incorreto.")

  itens_carrinho_db = carrinho_db.produto_no_carrinho()

  if len(itens_carrinho_db) != 1:
    raise RuntimeError("Carrinho retornou com quantidade inesperada de itens.")

  if itens_carrinho_db[0].produto.id_prod != produto.id_prod:
    raise RuntimeError("Produto_Carrinho retornou com produto incorreto.")

  print("[OK] Cliente foi lido novamente.")
  print("[OK] Cartão foi lido novamente.")
  print("[OK] Produto foi lido novamente.")
  print("[OK] Carrinho foi lido novamente com Produto_Carrinho.")

  print("\n--- DADOS PERSISTIDOS ---")
  print(f"Cliente: {cliente_db.to_dict()}")
  print(f"Cartão: {cartao_db.to_dict()}")
  print(f"Produto: {produto_db.to_dict()}")
  print(f"Carrinho: {carrinho_db.to_dict()}")
  print(f"Histórico: {historico}")

  # Um UPDATE de cada domínio/repository principal.
  cliente_db.nome = "TESTE FINAL MAIN - ATUALIZADO"
  cliente_repo.update(cliente_db.id_cli, cliente_db)

  produto_db.descricao = "Descrição atualizada pelo main de teste."
  produto_repo.update(produto_db.id_prod, produto_db)

  cartao_db.saldo = Decimal("900.00")
  cartao_repo.update(cartao_db.id_cartao, cartao_db)

  print("\n[OK] UPDATE de cliente realizado.")
  print("[OK] UPDATE de produto realizado.")
  print("[OK] UPDATE de cartão realizado.")

  cliente_final = cliente_repo.search(cliente.id_cli)
  produto_final = produto_repo.search(produto.id_prod)
  cartao_final = cartao_repo.search(cartao.id_cartao)

  if cliente_final is None or produto_final is None or cartao_final is None:
    raise RuntimeError("Falha ao ler os dados após os UPDATEs.")

  print("\n--- DADOS APÓS UPDATE ---")
  print(f"Cliente: {cliente_final.to_dict()}")
  print(f"Produto: {produto_final.to_dict()}")
  print(f"Cartão: {cartao_final.to_dict()}")

  return cliente.id_cli, produto.id_prod, cliente.carrinho.id_carrinho


def main() -> int:
  titulo("TESTE FINAL DE PERSISTÊNCIA")

  try:
    validar_configuracao()

    titulo("1/4 - MAPPERS")
    testar_mappers()

    titulo("2/4 - POSTGRESQL")
    testar_banco()

    titulo("3/4 - INSERT + SEARCH + UPDATE")
    cliente_id, produto_id, carrinho_id = salvar_dados()

    titulo("4/4 - RESULTADO")
    print("[OK] 1 Cliente persistido.")
    print("[OK] 1 Cartão persistido.")
    print("[OK] 1 Produto persistido.")
    print("[OK] 1 Carrinho persistido.")
    print("[OK] 1 Produto_Carrinho persistido.")
    print("[OK] 1 Historico_Compra persistido.")
    print("[OK] 1 Item_Historico persistido.")
    print("\nOs dados NÃO serão apagados.")
    print("IDs criados:")
    print(f"  Cliente: {cliente_id}")
    print(f"  Produto: {produto_id}")
    print(f"  Carrinho: {carrinho_id}")
    print("\nTESTE CONCLUÍDO COM SUCESSO.")
    return 0

  except Exception as exc:
    print("\n[ERRO] O teste falhou.")
    print(f"Tipo: {type(exc).__name__}")
    print(f"Detalhe: {exc}")
    return 1


if __name__ == "__main__":
  raise SystemExit(main())
