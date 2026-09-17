import os
from dotenv import load_dotenv
import psycopg2

load_dotenv(dotenv_path="project\.env")

def iniciar_connexao():
  try:
    conn = psycopg2.connect(
      dbname=os.getenv("DB_NAME"),
      user=os.getenv("DB_USER"),
      password=os.getenv("DB_PASSWORD"),
      host=os.getenv("DB_HOST"),
      port=os.getenv("DB_PORT")
    )
    return conn
  except Exception as e:
    print(f"erro inesperado {e}")
    return None
  except psycopg2.OperationalError as e:
    print(f"Erro ao se conectar ao Banco de Dados {e}")
    return None