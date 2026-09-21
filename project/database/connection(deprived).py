import psycopg
from psycopg import InterfaceError, DatabaseError
from os import getenv
from dotenv import load_dotenv

load_dotenv(r"project\.env")

def iniciar_conexao():
  try:
    conn = psycopg.connect(dbname=getenv("DB_NAME"), host=getenv("DB_HOST"), 
    port=getenv("DB_PORT"),user=getenv("DB_USR"),password=getenv("DB_PASSWORD"))
    return conn
  except DatabaseError as e:
    print(f"Houve algum erro no banco de dados: {e}")
    raise
  except InterfaceError as e:
    print(f"Houve um erro de interface: {e}")
    raise
  except Exception as e:
    print(f"Houve um ero inesperado: {e}")
