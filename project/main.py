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
if (PROJECT_ROOT / "project").exists():
  ROOT = PROJECT_ROOT
else:
  ROOT = PROJECT_ROOT.parent

if str(ROOT) not in sys.path:
  sys.path.insert(0, str(ROOT))

load_dotenv(ROOT / ".env")

REQUIRED_VARS = ("DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD")
EXPECTED_TABLES = {"cliente", "produto", "cartao", "historico_compra", "item_historico"}


def titulo(texto: str) -> None:
  print("\n" + "=" * 72)
  print(texto)
  print("=" * 72)


def validar_configuracao() -> bool:
  ausentes = [nome for nome in REQUIRED_VARS if not os.getenv(nome)]

  if ausentes:
    print("[ERRO] Variáveis ausentes no .env:")
    for nome in ausentes:
      print(f"  - {nome}")
    return False

  return True


def testar_mappers() -> None:
  from project.infra import entities  # noqa: F401
  configure_mappers()


def validar_schema(db) -> None:
  tabelas = db.session.execute(
    text("""
      SELECT table_name
      FROM information_schema.tables
      WHERE table_schema = 'public'
        AND table_name = ANY(:tables)
    """),
    {"tables": list(EXPECTED_TABLES)}
  ).scalars().all()

  faltando = EXPECTED_TABLES - set(tabelas)

  if faltando:
    raise RuntimeError(f"Tabelas ausentes no PostgreSQL: {', '.join(sorted(faltando))}")


def testar_fluxo_principal() -> tuple[int, int]:
  from project.domain.Cartao import Cartao
  from project.domain.Cliente import Cliente
  from project.domain.Produto import Produto
  from project.domain.ProcessadorPagamento import ProcessadorPagamento
  from project.infra.repository.Cartao_Repository import Cartao_Repository
  from project.infra.repository.Cliente_Repository import Cliente_Repository
  from project.infra.repository.Historico_Repository import Historico_Compra_Repository
  from project.infra.repository.Produto_Repository import Produto_Repository

  cliente_repo = Cliente_Repository()
  produto_repo = Produto_Repository()
  cartao_repo = Cartao_Repository()

  cliente = Cliente(
    nome="TESTE MAIN",
    idade=25,
    endereco="Endereco temporario do main",
    nacionalidade="Brasileira"
  )

  cartao = Cartao(
    numero="TESTE-MAIN-CARTAO",
    validade=date.today(),
    cvv="999",
    bandeira="TESTE",
    saldo=Decimal("1000.00")
  )

  cliente.inserir_cartao(cartao)

  assert cliente_repo.insert(cliente) is True
  assert cliente.id_cli is not None
  assert cartao.id_cartao is not None
  assert cartao.id_cli == cliente.id_cli
  print(f"[OK] Cliente inserido. id_cli = {cliente.id_cli}")
  print(f"[OK] Cartão inserido pelo relationship. id_cartao = {cartao.id_cartao}")

  produto = Produto(
    nome="PRODUTO TESTE MAIN",
    preco=Decimal("100.00"),
    descricao="Produto temporario do teste de integracao",
    estoque=10
  )

  assert produto_repo.insert(produto) is True
  assert produto.id_prod is not None
  print(f"[OK] Produto inserido. id_prod = {produto.id_prod}")

  cliente_banco = cliente_repo.search(cliente.id_cli)
  produto_banco = produto_repo.search(produto.id_prod)
  cartao_banco = cartao_repo.search(cartao.id_cartao)

  assert cliente_banco is not None
  assert cliente_banco.id_cli == cliente.id_cli
  assert produto_banco is not None
  assert produto_banco.id_prod == produto.id_prod
  assert cartao_banco is not None
  assert cartao_banco.id_cartao == cartao.id_cartao
  assert cartao_banco.id_cli == cliente.id_cli

  print("[OK] Cliente, produto e cartão foram lidos novamente pelos repositories.")

  cliente_domain_update = Cliente(
    nome="TESTE MAIN ATUALIZADO",
    idade=26,
    endereco="Endereco atualizado",
    nacionalidade="Brasileira",
    id_cli=cliente.id_cli
  )

  assert cliente_repo.update(cliente.id_cli, cliente_domain_update) is True
  cliente_banco = cliente_repo.search(cliente.id_cli)
  assert cliente_banco is not None
  assert cliente_banco.nome == "TESTE MAIN ATUALIZADO"
  print("[OK] UPDATE de cliente funcionando.")

  produto_domain_update = Produto(
    nome=produto.nome,
    preco=produto.preco,
    descricao="Descricao atualizada",
    estoque=produto.estoque,
    id_prod=produto.id_prod
  )

  assert produto_repo.update(produto.id_prod, produto_domain_update) is True
  produto_banco = produto_repo.search(produto.id_prod)
  assert produto_banco is not None
  assert produto_banco.descricao == "Descricao atualizada"
  produto.descricao = produto_banco.descricao
  print("[OK] UPDATE de produto funcionando.")

  cliente_carrinho = cliente_repo.search(cliente.id_cli)
  assert cliente_carrinho is not None
  assert len(cliente_carrinho.cartoes) == 1

  cartao_carrinho = cliente_carrinho.cartoes[0]
  produto_compra = produto_repo.search(produto.id_prod)
  assert produto_compra is not None

  cliente_carrinho.carrinho.adicionar_produto(produto_compra, 2)
  total = cliente_carrinho.carrinho.calcular_total()
  assert total == Decimal("200.00")
  print(f"[OK] Carrinho calculado. Total = R$ {total}")

  itens_compra = cliente_carrinho.carrinho.produto_no_carrinho()
  saldo_antes = cartao_carrinho.saldo
  estoque_antes = produto_compra.estoque

  ProcessadorPagamento.processarcompra(cliente_carrinho, cartao_carrinho.id_cartao)

  assert cartao_carrinho.saldo == saldo_antes - total
  assert produto_compra.estoque == estoque_antes - 2
  assert len(cliente_carrinho.carrinho.produto_no_carrinho()) == 0
  print("[OK] ProcessadorPagamento alterou saldo, estoque e limpou o carrinho.")

  assert cartao_repo.update(cartao_carrinho.id_cartao, cartao_carrinho) is True
  assert produto_repo.update(produto_compra.id_prod, produto_compra) is True
  print("[OK] Saldo e estoque atualizados no PostgreSQL pelos repositories.")

  assert Historico_Compra_Repository.registrar_compra(cliente_carrinho.id_cli, total, itens_compra) is True
  historicos = Historico_Compra_Repository.listar_por_cliente(cliente_carrinho.id_cli)
  assert historicos

  ultimo = historicos[0]
  assert ultimo["id_cli"] == cliente_carrinho.id_cli
  assert ultimo["valor_total"] == total
  assert len(ultimo["itens"]) == 1
  assert ultimo["itens"][0]["id_prod"] == produto_compra.id_prod
  assert ultimo["itens"][0]["quantidade"] == 2
  assert ultimo["itens"][0]["preco_momento"] == Decimal("100.00")

  historico_id = ultimo["id_historico"]
  print(f"[OK] historico_compra registrado. id_historico = {historico_id}")
  print("[OK] item_historico registrado com id_prod, quantidade e preco_momento.")

  return cliente.id_cli, produto.id_prod


def testar_erros_do_dominio() -> None:
  from project.domain.Cartao import Cartao
  from project.domain.Cliente import Cliente
  from project.domain.Produto import Produto
  from project.domain.ProcessadorPagamento import ProcessadorPagamento

  cliente = Cliente("TESTE ERROS", 20, "Endereco", "Brasileira")
  cartao = Cartao("TESTE-ERRO", date.today(), "111", "TESTE", Decimal("10.00"), id_cartao=999999)
  produto = Produto("Produto erro", Decimal("100.00"), "Teste", 1, id_prod=999999)
  cliente.inserir_cartao(cartao)

  try:
    ProcessadorPagamento.processarcompra(cliente, cartao.id_cartao)
    raise AssertionError("Pagamento com carrinho vazio deveria falhar.")
  except ValueError as exc:
    assert "carrinho" in str(exc).lower()

  cliente.carrinho.adicionar_produto(produto, 1)
  try:
    ProcessadorPagamento.processarcompra(cliente, cartao.id_cartao)
    raise AssertionError("Pagamento com saldo insuficiente deveria falhar.")
  except ValueError as exc:
    assert "saldo" in str(exc).lower()

  print("[OK] Regras de erro do ProcessadorPagamento continuam funcionando.")


def limpar_teste(cliente_id: int | None, produto_id: int | None) -> None:
  if cliente_id is None and produto_id is None:
    return

  from project.infra.repository.Cliente_Repository import Cliente_Repository
  from project.infra.repository.Produto_Repository import Produto_Repository

  try:
    if cliente_id is not None:
      Cliente_Repository().delete(cliente_id)
      print(f"[OK] Cliente de teste removido: {cliente_id}")
  except Exception as exc:
    print(f"[AVISO] Não foi possível remover o cliente de teste: {exc}")

  try:
    if produto_id is not None:
      Produto_Repository().delete(produto_id)
      print(f"[OK] Produto de teste removido: {produto_id}")
  except Exception as exc:
    print(f"[AVISO] Não foi possível remover o produto de teste: {exc}")


def main() -> int:
  titulo("TESTE DE INTEGRACAO - DOMAIN + REPOSITORIES + SQLALCHEMY + POSTGRESQL")

  if not validar_configuracao():
    return 1

  from project.infra.configs.connection import DBConnectionHandler

  cliente_id = None
  produto_id = None

  try:
    titulo("1/6 - MAPPERS DO SQLALCHEMY")
    testar_mappers()
    print("[OK] Todas as entities e relationships foram configuradas.")

    titulo("2/6 - CONEXAO COM POSTGRESQL")
    with DBConnectionHandler() as db:
      info = db.session.execute(text("SELECT current_database(), current_user, current_schema()")).one()
      print(f"[OK] Banco: {info[0]}")
      print(f"[OK] Usuário: {info[1]}")
      print(f"[OK] Schema: {info[2]}")
      validar_schema(db)
      print("[OK] As cinco tabelas esperadas existem no banco.")
      db.session.rollback()

    titulo("3/6 - REPOSITORIES / CRUD")
    cliente_id, produto_id = testar_fluxo_principal()
    print("[OK] INSERT + SEARCH + UPDATE executados pelos repositories.")

    titulo("4/6 - REGRAS DE NEGOCIO")
    testar_erros_do_dominio()

    titulo("5/6 - LIMPEZA DOS DADOS DE TESTE")
    limpar_teste(cliente_id, produto_id)
    cliente_id = None
    produto_id = None

    titulo("6/6 - RESULTADO")
    print("[OK] PostgreSQL respondeu.")
    print("[OK] Psycopg respondeu através do SQLAlchemy.")
    print("[OK] Relationships foram montados.")
    print("[OK] Cliente foi inserido e lido pelos repositories.")
    print("[OK] Produto foi inserido e lido pelos repositories.")
    print("[OK] Cartão foi inserido através do relationship do Cliente.")
    print("[OK] IDs SERIAL gerados pelo PostgreSQL foram recuperados.")
    print("[OK] UPDATEs funcionaram.")
    print("[OK] Carrinho e ProcessadorPagamento funcionaram.")
    print("[OK] historico_compra e item_historico foram gravados e lidos.")
    print("\nTESTE DE INTEGRACAO CONCLUIDO COM SUCESSO.")
    return 0

  except Exception as exc:
    print("\n[ERRO] O teste de integração falhou.")
    print(f"Tipo: {type(exc).__name__}")
    print(f"Detalhe: {exc}")
    return 1

  finally:
    limpar_teste(cliente_id, produto_id)


if __name__ == "__main__":
  raise SystemExit(main())
