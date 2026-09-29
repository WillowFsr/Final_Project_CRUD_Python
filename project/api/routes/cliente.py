from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from project.infra.repository.Cliente_Repository import Cliente_Repository

cliente_router = APIRouter(prefix="/clientes", tags=["Clientes"])

@cliente_router.post("/",status_code=status.HTTP_201_CREATED)
def criar_cliente():
  pass  