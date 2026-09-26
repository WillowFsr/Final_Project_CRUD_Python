from __future__ import annotations

import os
import sys
from decimal import Decimal
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.orm import configure_mappers


# Permite executar:
#   python project/main.py
# ou:
#   python -m project.main
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")


REQUIRED_VARS = (
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
)

# Este é o contrato do PostgreSQL que você me passou.
EXPECTED_SCHEMA = {
    "cliente": {
        "id_cli",
        "nome",
        "idade",
        "endereco",
        "nacionalidade",
    },
    "produto": {
        "id_prod",
        "nome",
        "preco",
        "descricao",
        "estoque",
    },
    "cartao": {
        "id_cartao",
        "id_cli",
        "numero",
        "validade",
        "cvv",
        "bandeira",
        "saldo",
    },
    "historico_compra": {
        "id_historico",
        "id_cli",
        "valor_total",
        "data_compra",
    },
    "item_historico": {
        "id_item",
        "id_historico",
        "id_prod",
        "quantidade",
        "preco_momento",
    },
}


def validar_configuracao() -> list[str]:
    return [nome for nome in REQUIRED_VARS if not os.getenv(nome)]


def mascarar_url() -> str:
    host = os.getenv("DB_HOST", "<ausente>")
    port = os.getenv("DB_PORT", "<ausente>")
    database = os.getenv("DB_NAME", "<ausente>")
    user = os.getenv("DB_USER", "<ausente>")
    return f"postgresql+psycopg://{user}:***@{host}:{port}/{database}"


def imprimir_titulo(texto: str) -> None:
    print("\n" + "=" * 72)
    print(texto)
    print("=" * 72)


def testar_mappers() -> None:
    """
    Garante que o SQLAlchemy consegue montar os relationships
    definidos nas entidades.
    """
    from project.infra import entities  # noqa: F401

    configure_mappers()


def ler_schema(db) -> dict[str, set[str]]:
    rows = db.session.execute(
        text(
            """
            SELECT table_name, column_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = ANY(:tables)
            ORDER BY table_name, ordinal_position
            """
        ),
        {"tables": list(EXPECTED_SCHEMA.keys())},
    ).all()

    schema: dict[str, set[str]] = {}
    for table_name, column_name in rows:
        schema.setdefault(table_name, set()).add(column_name)

    return schema


def validar_schema(db) -> list[str]:
    schema = ler_schema(db)
    erros: list[str] = []

    for table, expected_columns in EXPECTED_SCHEMA.items():
        actual_columns = schema.get(table)

        if actual_columns is None:
            erros.append(f"Tabela ausente: {table}")
            continue

        faltando = expected_columns - actual_columns
        if faltando:
            erros.append(
                f"{table}: colunas ausentes -> {', '.join(sorted(faltando))}"
            )

    return erros


def teste_roundtrip_transacional(db) -> None:
    """
    Testa escrita + leitura + relacionamentos diretamente no PostgreSQL,
    mas faz ROLLBACK no final. Assim, nenhum dado de teste fica salvo.
    """
    cliente_id = db.session.execute(
        text(
            """
            INSERT INTO cliente (
                nome,
                idade,
                endereco,
                nacionalidade
            )
            VALUES (
                :nome,
                :idade,
                :endereco,
                :nacionalidade
            )
            RETURNING id_cli
            """
        ),
        {
            "nome": "TESTE CONEXAO",
            "idade": 30,
            "endereco": "TESTE - NAO SALVAR",
            "nacionalidade": "Brasileira",
        },
    ).scalar_one()

    produto_id = db.session.execute(
        text(
            """
            INSERT INTO produto (
                nome,
                preco,
                descricao,
                estoque
            )
            VALUES (
                :nome,
                :preco,
                :descricao,
                :estoque
            )
            RETURNING id_prod
            """
        ),
        {
            "nome": "PRODUTO TESTE CONEXAO",
            "preco": Decimal("49.90"),
            "descricao": "Registro temporario do teste do main",
            "estoque": 10,
        },
    ).scalar_one()

    cartao_id = db.session.execute(
        text(
            """
            INSERT INTO cartao (
                id_cli,
                numero,
                validade,
                cvv,
                bandeira,
                saldo
            )
            VALUES (
                :id_cli,
                :numero,
                CURRENT_DATE,
                :cvv,
                :bandeira,
                :saldo
            )
            RETURNING id_cartao
            """
        ),
        {
            "id_cli": cliente_id,
            "numero": "TESTE-CARTAO-CONEXAO",
            "cvv": "000",
            "bandeira": "TESTE",
            "saldo": Decimal("1000.00"),
        },
    ).scalar_one()

    historico_id = db.session.execute(
        text(
            """
            INSERT INTO historico_compra (
                id_cli,
                valor_total
            )
            VALUES (
                :id_cli,
                :valor_total
            )
            RETURNING id_historico
            """
        ),
        {
            "id_cli": cliente_id,
            "valor_total": Decimal("99.80"),
        },
    ).scalar_one()

    item_id = db.session.execute(
        text(
            """
            INSERT INTO item_historico (
                id_historico,
                id_prod,
                quantidade,
                preco_momento
            )
            VALUES (
                :id_historico,
                :id_prod,
                :quantidade,
                :preco_momento
            )
            RETURNING id_item
            """
        ),
        {
            "id_historico": historico_id,
            "id_prod": produto_id,
            "quantidade": 2,
            "preco_momento": Decimal("49.90"),
        },
    ).scalar_one()

    resultado = db.session.execute(
        text(
            """
            SELECT
                c.id_cli,
                c.nome,
                p.id_prod,
                p.preco,
                ca.id_cartao,
                hc.id_historico,
                hc.valor_total,
                ih.id_item,
                ih.quantidade,
                ih.preco_momento
            FROM cliente c
            JOIN cartao ca
              ON ca.id_cli = c.id_cli
            JOIN historico_compra hc
              ON hc.id_cli = c.id_cli
            JOIN item_historico ih
              ON ih.id_historico = hc.id_historico
            JOIN produto p
              ON p.id_prod = ih.id_prod
            WHERE c.id_cli = :id_cli
              AND p.id_prod = :id_prod
              AND ca.id_cartao = :id_cartao
              AND hc.id_historico = :id_historico
              AND ih.id_item = :id_item
            """
        ),
        {
            "id_cli": cliente_id,
            "id_prod": produto_id,
            "id_cartao": cartao_id,
            "id_historico": historico_id,
            "id_item": item_id,
        },
    ).mappings().one()

    assert resultado["id_cli"] == cliente_id
    assert resultado["id_prod"] == produto_id
    assert resultado["id_cartao"] == cartao_id
    assert resultado["id_historico"] == historico_id
    assert resultado["id_item"] == item_id
    assert resultado["preco"] == Decimal("49.90")
    assert resultado["valor_total"] == Decimal("99.80")
    assert resultado["quantidade"] == 2
    assert resultado["preco_momento"] == Decimal("49.90")

    # Muito importante: não deixa registros de teste persistirem.
    db.session.rollback()


def testar_conexao_completa() -> int:
    imprimir_titulo("TESTE COMPLETO DO POSTGRESQL")

    print(f"Projeto:       {PROJECT_ROOT}")
    print(f"Arquivo .env:  {PROJECT_ROOT / '.env'}")
    print(f"Connection URL: {mascarar_url()}")

    ausentes = validar_configuracao()
    if ausentes:
        print("\n[ERRO] Configuração incompleta:")
        for nome in ausentes:
            print(f"  - {nome}")
        return 1

    try:
        # Importa exatamente o handler usado pelo restante da aplicação.
        from project.infra.configs.connection import DBConnectionHandler
    except ModuleNotFoundError as exc:
        print("\n[ERRO] Dependência ausente.")
        print(f"Detalhe: {exc}")
        print("\nExecute:")
        print("  python -m pip install -r requirements.txt")
        return 1

    try:
        imprimir_titulo("1/4 - SQLALCHEMY / MAPPERS")
        testar_mappers()
        print("[OK] Entidades e relationships carregados sem erro.")

        imprimir_titulo("2/4 - CONEXAO")
        with DBConnectionHandler() as db:
            info = db.session.execute(
                text(
                    """
                    SELECT
                        current_database() AS banco,
                        current_user AS usuario,
                        current_schema() AS schema_atual,
                        version() AS versao
                    """
                )
            ).mappings().one()

            print("[OK] PostgreSQL conectado.")
            print(f"Banco:    {info['banco']}")
            print(f"Usuário:  {info['usuario']}")
            print(f"Schema:   {info['schema_atual']}")
            print(f"Versão:   {info['versao']}")

            imprimir_titulo("3/4 - ESTRUTURA DO BANCO")
            erros_schema = validar_schema(db)

            if erros_schema:
                print("[ERRO] O código espera uma estrutura diferente do banco:")
                for erro in erros_schema:
                    print(f"  - {erro}")
                db.session.rollback()
                return 1

            print("[OK] As 5 tabelas e suas colunas principais foram encontradas.")

            imprimir_titulo("4/5 - TESTE ORM / SQLALCHEMY")
            from project.infra.entities import (
                Cliente,
                Cartao,
                Produto,
                Historico_Compra,
                Item_Historico_Compra,
            )

            entidades = {
                "cliente": Cliente,
                "cartao": Cartao,
                "produto": Produto,
                "historico_compra": Historico_Compra,
                "item_historico": Item_Historico_Compra,
            }

            for nome, entidade in entidades.items():
                quantidade = db.session.query(entidade).count()
                print(f"[OK] ORM consultou {nome}: {quantidade} registro(s).")

            imprimir_titulo("5/5 - TESTE REAL DE ESCRITA/LEITURA")
            print("Inserindo registros temporários...")
            teste_roundtrip_transacional(db)
            print("[OK] INSERT + FOREIGN KEYS + JOIN + SELECT funcionaram.")
            print("[OK] Dados de teste foram revertidos com ROLLBACK.")


        imprimir_titulo("RESULTADO")
        print("[OK] A comunicação com o PostgreSQL está funcionando.")
        print("[OK] SQLAlchemy está funcionando.")
        print("[OK] Psycopg está funcionando.")
        print("[OK] O schema esperado foi encontrado.")
        print("[OK] A aplicação conseguiu escrever e ler dados relacionados.")
        print("\nSeu banco respondeu a um teste de ponta a ponta.")
        return 0

    except Exception as exc:
        print("\n[ERRO] O teste falhou.")
        print(f"Tipo:    {type(exc).__name__}")
        print(f"Detalhe: {exc}")
        print("\nNenhum dado de teste deve ser considerado persistido.")
        return 1


if __name__ == "__main__":
    raise SystemExit(testar_conexao_completa())
