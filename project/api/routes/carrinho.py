from __future__ import annotations
from fastapi import APIRouter, HTTPException, status, Path

#Carrinho Stuff
from project.api.schemas.carrinho_schema import CarrinhoResponse, ProdutoCarrinhoRequest
from project.infra.repository.Carrinho_Repository import Carrinho_Repository

#Produto Stuff
from project.infra.repository.Produto_Repository import Produto_Repository

#Cliente stuff
from project.infra.repository.Cliente_Repository import Cliente_Repository

carrinho_router = APIRouter(prefix="/clientes/{id_cli}/carrinho", tags=["Carrinho"])


@carrinho_router.post("/itens",response_model=CarrinhoResponse,status_code=status.HTTP_200_OK)
def adicionar_item_carrinho(item:ProdutoCarrinhoRequest,id_cli:int=Path(ge=1))-> CarrinhoResponse:
  cliente = Cliente_Repository().search(id_cli)
  if (not cliente):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente nao encontrado")
  
  produto = Produto_Repository().search(item.id_prod)
  
  if (not produto):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado")
  
  carrinho = Carrinho_Repository().search_by_cli(id_cli=id_cli)
  
  if (not carrinho):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Houve um erro no carrinho")
  
  carrinho.adicionar_produto(produto=produto,quantidade=item.quantidade)
  
  if (not Carrinho_Repository().update(carrinho)):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Houve um erro durante a atualizacao do carrinho")
  
  return carrinho

@carrinho_router.get("/{id_carrinho}", response_model=CarrinhoResponse, status_code=status.HTTP_200_OK)
def buscar_carrinho(id_cli:int=Path(ge=1),id_carrinho:int=Path(ge=1)) -> CarrinhoResponse:
  carrinho = Carrinho_Repository().search(id_carrinho)
  
  if (not carrinho):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrinho nao encontrado")
  
  if (carrinho.id_cli != id_cli):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Este cliente nao possui o id desse carrinho")
  
  return carrinho

@carrinho_router.delete("/itens/{id_prod}",status_code=status.HTTP_204_NO_CONTENT)
def remover_item_carrinho(id_cli:int=Path(ge=1), id_prod:int = Path(ge=1)) -> None:
  carrinho = Carrinho_Repository().search_by_cli(id_cli=id_cli)
  
  if (not carrinho):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrinho de cliente nao encontrado")
  
  produto = Produto_Repository().search(id_prod)
  
  if (not produto):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado")
  
  try:
    carrinho.remover_produto(produto=produto)
  except ValueError:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado neste carrinho")
  
  if (not Carrinho_Repository().update(carrinho)):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nao foi possivel atualizar o carrinho")
  
  return None