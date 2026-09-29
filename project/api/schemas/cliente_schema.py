from project.api.schemas.Base import Base
from pydantic import ConfigDict, Field

class ClienteBase(Base):
  nome: str = Field(min_length=1, max_length=150)
  idade: int = Field(ge=1)
  endereco: str = Field(min_length=1)
  nacionalidade: str = Field(min_length=1, max_length=25)

class ClienteRequest(ClienteBase):
  pass


class ClienteResponse(ClienteBase):
  model_config = ConfigDict(from_attributes=True)
  
  id_cli: int = Field(ge=1)
  