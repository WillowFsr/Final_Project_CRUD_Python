from __future__ import annotations

from project.api.schemas.produto_schema import ProdutoRequest,ProdutoResponse, EstoqueRequest
from fastapi import APIRouter, HTTPException, status, Path

from project.infra.repository.Produto_Repository import Produto_Repository
from project.domain.Produto import Produto as Produto_Domain

from project.application.use_cases.AumentarEstoque import AdicionarEstoque
from project.application.use_cases.RemoverEstoque import RemoverEstoque


produto_router = APIRouter(prefix="/produtos", tags=["Produtos"])

@produto_router.post("",response_model=ProdutoResponse,status_code=status.HTTP_201_CREATED)
def criar_produto(produto:ProdutoRequest) ->ProdutoResponse:
  novo_produto = Produto_Domain(nome=produto.nome,preco=produto.preco,descricao=produto.descricao,estoque=produto.estoque)
  
  if (not Produto_Repository().insert(novo_produto)):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Informacoes Invalidas")
  
  return novo_produto


@produto_router.get("/{id_prod}", response_model=ProdutoResponse, status_code=status.HTTP_200_OK)
def buscar_produto(id_prod:int = Path(ge=1)) -> ProdutoResponse:
  produto = Produto_Repository().search(id_prod)
  
  if (not produto):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Produto nao encontrado")
  
  return produto


@produto_router.put("/{id_prod}", response_model=ProdutoResponse, status_code=status.HTTP_200_OK)
def atualizar_produto(produto:ProdutoRequest,id_prod:int = Path(ge=1))-> ProdutoResponse:
  produto_atualizado = Produto_Domain(nome=produto.nome,preco=produto.preco,descricao=produto.descricao,estoque=produto.estoque, id_prod=id_prod)
  
  if (not Produto_Repository().update(id_prod,produto_atualizado)):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado")
  
  return produto_atualizado


@produto_router.delete("/{id_prod}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_produto(id_prod:int = Path(ge=1))-> None:
  if (not Produto_Repository().delete(id_prod)):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado ou nao existente")
  
  return None

@produto_router.post("/{id_prod}/estoque", status_code=status.HTTP_200_OK, response_model=ProdutoResponse)
def adicionar_estoque(estoque:EstoqueRequest,id_prod:int = Path(ge=1)) -> ProdutoResponse:
  produto = Produto_Repository().search(id_prod)
  
  if (not produto):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Produto nao encontrado")
  
  if (not AdicionarEstoque().adicionar_estoque(id_prod=id_prod,quantidade=estoque.quantidade)):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nao foi possivel aumentar o estoque")
  
  return Produto_Repository().search(id_prod)


@produto_router.post("/{id_prod}/estoque/remover",status_code=status.HTTP_200_OK, response_model=ProdutoResponse)
def remover_estoque(estoque:EstoqueRequest,id_prod:int = Path(ge=1)) -> ProdutoResponse:
  produto = Produto_Repository().search(id_prod)
  
  if (not produto):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Produto nao encontrado")
  
  if (produto.estoque < estoque.quantidade):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Estoque insuficiente")
  
  if (not RemoverEstoque().remover_estoque(id_prod=id_prod,quantidade=estoque.quantidade)):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nao foi possivel remover o estoque")
  
  return Produto_Repository().search(id_prod)


@produto_router.get("", response_model=list[ProdutoResponse])
def listar_produtos():
    return Produto_Repository().list_all()