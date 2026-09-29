from __future__ import annotations
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Path

from project.domain.Cliente import Cliente as Cliente_Domain
from project.infra.repository.Cliente_Repository import Cliente_Repository
from project.api.schemas.cliente_schema import ClienteRequest, ClienteResponse


cliente_router = APIRouter(prefix="/clientes", tags=["Clientes"])


## Cliente base routers, it serves the "CRUD" operations

@cliente_router.post("/",response_model=ClienteResponse,status_code=status.HTTP_201_CREATED)
def criar_cliente(cliente:ClienteRequest)-> ClienteResponse:
  novo_cliente = Cliente_Domain(nome=cliente.nome,idade=cliente.idade,endereco=cliente.endereco,nacionalidade=cliente.nacionalidade)
  
  if (not Cliente_Repository().insert(novo_cliente)):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Informacoes Invalidas")
  
  return novo_cliente

@cliente_router.get("/{id_cli}", response_model= ClienteResponse, status_code=status.HTTP_200_OK)
def buscar_cliente(id_cli:int = Path(ge=1)) -> ClienteResponse:
  cliente = Cliente_Repository().search(id_cli)
  
  if (not cliente):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cliente nao encontrado")
  
  return cliente

@cliente_router.put("/{id_cli}", response_model=ClienteResponse, status_code=status.HTTP_200_OK)
def atualizar_cliente(cliente:ClienteRequest, id_cli:int = Path(ge=1)) -> ClienteResponse:
  cliente_atualizar = Cliente_Domain(nome=cliente.nome,idade=cliente.idade,endereco=cliente.endereco,nacionalidade=cliente.nacionalidade, id_cli=id_cli)
  
  if (not Cliente_Repository().update(id_cli,cliente_atualizar)):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cliente nao encontrado")
  
  return cliente_atualizar    

@cliente_router.delete("/{id_cli}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_cliente(id_cli:int =Path(ge=1)) -> None:
  if (not Cliente_Repository().delete(id_cli)):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuario nao encontrado")

  return None
