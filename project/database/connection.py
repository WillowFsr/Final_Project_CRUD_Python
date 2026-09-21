from dotenv import load_dotenv
from os import getenv
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InterfaceError, DatabaseError

load_dotenv(r"project\.env")


try:
  engine = create_engine(f"postgresql+psycopg://{getenv('BD_USR')}:{getenv('DB_PASSWORD')}@{getenv('DB_HOST')}:{getenv('DB_PORxT')}/{getenv('DB_NAME')}")
except (InterfaceError, DatabaseError) as e:
  print(f"Ocorreu um erro: {e}")
except Exception as e:
  print(f"Ocorreu um erro inesperado: {e}")

Session = sessionmaker(engine)

@contextmanager
def get_connection():
  session = Session()
  try:
    pass
  finally:
    session.close()
