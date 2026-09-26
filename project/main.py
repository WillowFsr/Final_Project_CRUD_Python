from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import text


# Permite executar tanto:
#   python project/main.py
# quanto:
#   python -m project.main
PROJECT_ROOT = Path(__file__).resolve().parent
if PROJECT_ROOT.name == "project":
    PROJECT_ROOT = PROJECT_ROOT.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# Carrega o .env pela localização real do projeto, independentemente
# do diretório de onde o comando foi executado.
env_path = PROJECT_ROOT / ".env"
load_dotenv(env_path)


REQUIRED_VARS = (
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
)


def validar_configuracao() -> list[str]:
    """Retorna as variáveis de ambiente obrigatórias que estão ausentes."""
    return [nome for nome in REQUIRED_VARS if not os.getenv(nome)]


def mascarar_url() -> str:
    """Monta uma descrição segura da configuração sem exibir a senha."""
    host = os.getenv("DB_HOST", "<ausente>")
    port = os.getenv("DB_PORT", "<ausente>")
    database = os.getenv("DB_NAME", "<ausente>")
    user = os.getenv("DB_USER", "<ausente>")
    return f"postgresql+psycopg://{user}:***@{host}:{port}/{database}"


def testar_conexao() -> int:
    print("=" * 60)
    print("TESTE DE CONEXÃO - POSTGRESQL")
    print("=" * 60)
    print(f"Arquivo .env: {env_path}")
    print(f"Configuração: {mascarar_url()}")

    ausentes = validar_configuracao()
    if ausentes:
        print("\n[ERRO] Variáveis de ambiente ausentes:")
        for nome in ausentes:
            print(f"  - {nome}")
        return 1

    try:
        # Importa o mesmo handler usado pelos repositories do projeto.
        from project.infra.configs.connection import DBConnectionHandler
    except ModuleNotFoundError as exc:
        print("\n[ERRO] Dependência/import do projeto não disponível.")
        print(f"Detalhe: {exc}")
        print("\nInstale as dependências com:")
        print("  python -m pip install -r requirements.txt")
        return 1
    except Exception as exc:
        print("\n[ERRO] Não foi possível carregar a configuração de conexão.")
        print(f"Tipo: {type(exc).__name__}")
        print(f"Detalhe: {exc}")
        return 1

    try:
        with DBConnectionHandler() as db:
            resultado = db.session.execute(
                text(
                    """
                    SELECT
                        1 AS teste,
                        current_database() AS banco,
                        current_user AS usuario,
                        current_schema() AS schema_atual,
                        version() AS versao
                    """
                )
            ).mappings().one()

        print("\n[OK] Conexão com PostgreSQL estabelecida!")
        print(f"  Banco:    {resultado['banco']}")
        print(f"  Usuário:  {resultado['usuario']}")
        print(f"  Schema:   {resultado['schema_atual']}")
        print(f"  SELECT 1: {resultado['teste']}")
        print(f"  Versão:   {resultado['versao']}")
        print("\nO SQLAlchemy + psycopg está conseguindo acessar o banco.")
        return 0

    except ModuleNotFoundError as exc:
        print("\n[ERRO] O driver do PostgreSQL não está disponível.")
        print(f"Detalhe: {exc}")
        print("\nInstale o Psycopg 3 com:")
        print('  python -m pip install "psycopg[binary]"')
        return 1

    except Exception as exc:
        print("\n[ERRO] Não foi possível conectar ao PostgreSQL.")
        print(f"Tipo: {type(exc).__name__}")
        print(f"Detalhe: {exc}")
        print("\nVerifique principalmente:")
        print("  1. PostgreSQL está em execução.")
        print("  2. DB_HOST e DB_PORT estão corretos.")
        print("  3. DB_NAME existe.")
        print("  4. DB_USER e DB_PASSWORD estão corretos.")
        print("  5. O usuário possui permissão para acessar o banco.")
        return 1


if __name__ == "__main__":
    raise SystemExit(testar_conexao())
