from dotenv import load_dotenv
from os import getenv

from sqlalchemy.exc import InterfaceError, DatabaseError


load_dotenv(r"project\.env")
def iniciar_conexao():
  try:
    engine = create_engine(f"postgresql+psycopg://{getenv(BD_USR)}:{getenv(DB_PORT)}@{getenv(DB_HOST)/{getenv(DB_NAME)}}/")

  except InterfaceError as e:
    print(f"Ocorreu um erro de interface: {e}")
  
  except DatabaseError as e:
    print(f"Ocorreu um erro no banco de dados: {e}")

  except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")

