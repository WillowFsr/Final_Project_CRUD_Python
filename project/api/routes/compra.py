from __future__ import annotations

from fastapi import APIRouter, status, Path, HTTPException
from project.api.schemas.compra_schema import CompraRequest
from project.application.use_cases.RealizarCompra import RealizarCompra

compra_router = APIRouter(prefix="/clientes/{id_cli}/compras", tags=["Compras"])

@compra_router.post("", status_code=status.HTTP_204_NO_CONTENT)
def realizar_compra(compra:CompraRequest,id_cli:int=Path(ge=1))-> None:
  if (not RealizarCompra().realizar_compra(id_cliente=id_cli,id_cartao=compra.id_cartao)):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nao foi possivel efetuar a compra")
  
  return None
  