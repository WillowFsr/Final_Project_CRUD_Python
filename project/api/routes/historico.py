from typing import Annotated

from fastapi import APIRouter, Depends, status
from project.infra.repository.Historico_Repository import Historico_Compra_Repository

historico_router = APIRouter(prefix="/historico", tags=["Historico"])

@historico_router.post("/", status_code=status.HTTP_201_CREATED)
def criar_historico():
  pass