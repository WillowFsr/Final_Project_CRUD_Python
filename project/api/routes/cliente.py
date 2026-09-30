from __future__ import annotations
from fastapi import APIRouter, HTTPException, status, Path

#CLiente stuff
from project.domain.Cliente import Cliente as Cliente_Domain
from project.infra.repository.Cliente_Repository import Cliente_Repository
from project.api.schemas.cliente_schema import ClienteRequest, ClienteResponse

#Cartao stuff
from project.domain.Cartao import Cartao as Cartao_Domain
from project.infra.repository.Cartao_Repository import Cartao_Repository
from project.api.schemas.cartao import CartaoRequest,CartaoResponse

cliente_router = APIRouter(prefix="/clientes", tags=["Clientes"])


## Cliente base routers, it serves the "CRUD" operations
@cliente_router.post("",response_model=ClienteResponse,status_code=status.HTTP_201_CREATED)
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

# Cartao Routes as a Cliente sub-resource

@cliente_router.post("/{id_cli}/cartoes", response_model=CartaoResponse,status_code=status.HTTP_201_CREATED)
def criar_cartao(cartao:CartaoRequest, id_cli:int =Path(ge=1)) -> CartaoResponse:
  cliente = Cliente_Repository().search(id_cli)
  
  if (not cliente):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cliente nao encontrado")
  
  novo_cartao = Cartao_Domain(numero=cartao.numero,validade=cartao.validade,cvv=cartao.cvv,bandeira=cartao.bandeira,id_cli=id_cli)
  
  if (not Cartao_Repository().insert(novo_cartao)):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Informacoes invalidas")
  
  return novo_cartao

@cliente_router.get("/{id_cli}/cartoes/{id_cartao}", response_model=CartaoResponse, status_code=status.HTTP_200_OK)
def buscar_cartao_cliente(id_cli:int = Path(ge=1), id_cartao:int = Path(ge=1))-> CartaoResponse:
  cliente = Cliente_Repository().search(id_cli)
  
  if (not cliente):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cliente nao encontrado")
  
  cartao_busca = Cartao_Repository().search(id_cartao)
   
  if (not cartao_busca):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cartao nao encontrado")
  
  if (cartao_busca.id_cli != id_cli):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cartao nao pertence ao cliente informado")
  
  return cartao_busca
 
@cliente_router.put("/{id_cli}/cartoes/{id_cartao}", response_model= CartaoResponse, status_code=status.HTTP_200_OK)
def atualizar_cartao_cliente(cartao:CartaoRequest,id_cli:int = Path(ge=1), id_cartao:int = Path(ge=1))-> CartaoResponse:
  cliente = Cliente_Repository().search(id_cli)
  
  if (not cliente):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cliente nao encontrado")
  
  cartao_atual = Cartao_Repository().search(id_cartao)
  
  if (not cartao_atual):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cartao nao encontrado")
  
  if (cartao_atual.id_cli != id_cli):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cliente nao possui este cartao")
  
  cartao_atualizar = Cartao_Domain(numero=cartao.numero,validade=cartao.validade,cvv=cartao.cvv,bandeira=cartao.bandeira,id_cli=id_cli, id_cartao=id_cartao)
  
  if (not Cartao_Repository().update(id_cartao,cartao_atualizar)):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Informacoes incorretas")
  
  return cartao_atualizar
  
@cliente_router.delete("/{id_cli}/cartoes/{id_cartao}",status_code=status.HTTP_204_NO_CONTENT)
def excluir_cartao_cliente(id_cli:int =Path(ge=1), id_cartao:int = Path(ge=1))-> None:
  cliente = Cliente_Repository().search(id_cli)
  
  if (not cliente):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cliente nao encontrado")
  
  cartao = Cartao_Repository().search(id_cartao)
  
  if (not cartao):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cartao nao encontrado")
  
  if (cartao.id_cli != id_cli):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cliente nao possui este cartao")
  
  if (not Cartao_Repository().delete(id_cartao)):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Nao foi possivel excluir o cartao")
  
  return None