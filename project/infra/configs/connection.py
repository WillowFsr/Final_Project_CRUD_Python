from dotenv import load_dotenv
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(r'.env')

class DBConnectionHandler:
  def __init__(self) -> None:
    self.__connection_string = f"postgresql+psycopg://{getenv('DB_USER')}:{getenv('DB_PASSWORD')}@{getenv('DB_HOST')}:{getenv('DB_PORT')}/{getenv('DB_NAME')}"

    self.__engine = self._create_database_engine()
    self.session = None


  def _create_database_engine(self):
    engine = create_engine(self.__connection_string)
    return engine

  #when this class is created, it will run this code, creating a new session and returning actual context of it for use, after this, session will be return as None
  def __enter__(self):
    LocalSession = sessionmaker(bind=self.__engine)
    self.session = LocalSession()
    return self 

  #when finished the code, it will close session and do the commit automatically when exit >,<
  def __exit__(self,exc_type,exc_val, exc_tb):
    try:
      if exc_type:
        self.session.rollback()
      else:
        self.session.commit()
    except Exception as e:
      print(f"Ocorreu um erro: {e}")
      self.session.rollback()
      raise e
    finally:
      self.session.close()

    
  #if we need use raw sql(most cases no), just in case
  def get_engine(self):
    return self.__engine
