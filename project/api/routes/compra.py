from typing import Annotated

from fastapi import APIRouter, Depends, status
from project.application.use_cases.RealizarCompra import RealizarCompra

compra_router = APIRouter(prefix="/compra", tags=["Compra"])

@compra_router.post("/", status_code=status.HTTP_201_CREATED)
def criar_compra():
  pass


