from dotenv import load_dotenv
from os import getenv
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InterfaceError, DatabaseError
from sqlalchemy.ext.declarative import declarative_base

load_dotenv(r"project\.env")  

#the engine its a lazy starter, it dont starts the connection automatically, so.. dont need to check, only need on session
engine = create_engine(f"postgresql+psycopg://{getenv('BD_USR')}:{getenv('DB_PASSWORD')}@{getenv('DB_HOST')}:{getenv('DB_PORT')}/{getenv('DB_NAME')}")

Base = declarative_base()

#the actual connection, it uses orm to get connection
SessionLocal = sessionmaker(bind=engine)

#the context manager its a form to use with open with other type of writing
@contextmanager
def get_connection():
  session = SessionLocal()
  try:
    #when the function are called, it will return in the end session.commit and after that session.close when operations are done
    yield session
    session.commit()
  except (Exception, DatabaseError, InterfaceError) as e:
    session.rollback()
    print(f"Houve um erro: {e}")
    raise
  finally:
    session.close()
  