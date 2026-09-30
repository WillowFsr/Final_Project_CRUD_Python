from __future__ import annotations

from project.api.schemas.produto_schema import ProdutoRequest,ProdutoResponse
from fastapi import APIRouter, HTTPException, status, Path
from project.infra.repository.Produto_Repository import Produto_Repository
from project.domain.Produto import Produto as Produto_Domain

produto_router = APIRouter(prefix="/produtos", tags=["Produtos"])

@produto_router.post("",response_model=ProdutoResponse,status_code=status.HTTP_201_CREATED)
def criar_produto(produto:ProdutoRequest) ->ProdutoResponse:
  novo_produto = Produto_Domain(nome=produto.nome,preco=produto.preco,descricao=produto.descricao,estoque=produto.estoque)
  
  if (not Produto_Repository().insert(novo_produto)):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Informacoes Invalidas")
  
  return novo_produto


@produto_router.get("/{id_produto}", response_model=ProdutoResponse, status_code=status.HTTP_200_OK)
def buscar_produto(id_produto:int = Path(ge=1)) -> ProdutoResponse:
  produto = Produto_Repository().search(id_produto)
  
  if (not produto):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Produto nao encontrado")
  
  return produto

@produto_router.put("/{id_produto}", response_model=ProdutoResponse, status_code=status.HTTP_200_OK)
def atualizar_produto(produto:ProdutoRequest,id_produto:int = Path(ge=1))-> ProdutoResponse:
  produto_atualizado = Produto_Domain(nome=produto.nome,preco=produto.preco,descricao=produto.descricao,estoque=produto.estoque, id_prod=id_produto)
  
  if (not Produto_Repository().update(id_produto,produto_atualizado)):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Produto nao encontrado")
  
  return produto_atualizado

@produto_router.delete("/{id_produto}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_produto(id_produto:int = Path(ge=1))-> None:
  if (not Produto_Repository().delete(id_produto)):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Produto nao encontrado ou nao existente")
  
  return None