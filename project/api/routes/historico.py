from __future__ import annotations

from fastapi import APIRouter, Path, status, HTTPException
from project.infra.repository.Historico_Repository import Historico_Compra_Repository
from project.infra.repository.Cliente_Repository import Cliente_Repository
from project.api.schemas.historico_schema import Item_Historico_Response, HistoricoResponse

historico_router = APIRouter(prefix="/clientes/{id_cli}/historico", tags=["Historico"])

@historico_router.get("",status_code=status.HTTP_200_OK, response_model= list[HistoricoResponse])
def listar_historico_cliente(id_cli:int =Path(ge=1)) -> list[HistoricoResponse]:
  cliente = Cliente_Repository().search(id_cli)
  
  if (not cliente):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente nao encontrado")
  
  return Historico_Compra_Repository().listar_por_cliente(id_cli=id_cli)


@historico_router.get("/{id_historico}", status_code=status.HTTP_200_OK,response_model=HistoricoResponse)
def listar_por_id(id_cli:int =Path(ge=1),id_historico:int=Path(ge=1)) -> HistoricoResponse:
  historico = Historico_Compra_Repository().buscar_por_id(id_historico)
  
  if (not historico):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Historico nao Enconrado")
  
  if (historico["id_cli"] != id_cli):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Esse historico nao pertence a esse cliente")
  
  return historico  