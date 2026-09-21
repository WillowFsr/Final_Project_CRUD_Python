from dotenv import load_dotenv
from os import getenv
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InterfaceError, DatabaseError
from sqlalchemy.ext.declarative import declarative_base

load_dotenv(r"project\.env")

engine = create_engine(f"postgresql+psycopg://{getenv('BD_USR')}:{getenv('DB_PASSWORD')}@{getenv('DB_HOST')}:{getenv('DB_PORT')}/{getenv('DB_NAME')}")

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

@contextmanager
def get_connection():
  session = SessionLocal()
  try:
    yield session
    session.commit()
  except (Exception, DatabaseError, InterfaceError) as e:
    session.rollback()
    print(f"Houve um erro: {e}")
    raise
  finally:
    session.close()
