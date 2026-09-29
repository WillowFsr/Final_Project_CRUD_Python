from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from project.infra.repository.Produto_Repository import Produto_Repository

produto_router = APIRouter(prefix="/produtos", tags=["Produtos"])

@produto_router.post("/", status_code=status.HTTP_201_CREATED)
def criar_produto():
  pass