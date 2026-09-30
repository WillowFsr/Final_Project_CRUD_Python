from project.api.schemas.Base import Base
from pydantic import Field
from decimal import Decimal
from datetime import datetime


class Item_Historico_Response(Base):
  id_item: int = Field(ge=1)
  id_prod: int = Field(ge=1)
  quantidade: int = Field(ge=1)
  preco_momento: Decimal = Field(ge=Decimal("0.00"))


class HistoricoResponse(Base):
  id_historico: int = Field(ge=1)
  id_cli: int = Field(ge=1)
  valor_total: Decimal = Field(ge=Decimal("0.00"))
  data_compra: datetime
  itens: list["Item_Historico_Response"]