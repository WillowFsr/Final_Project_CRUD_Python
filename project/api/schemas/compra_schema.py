from project.api.schemas.Base import Base

from pydantic import Field


class CompraRequest(Base):
  id_cartao: int = Field(ge=1)