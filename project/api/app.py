from fastapi import FastAPI
from project.api.routes.cliente import cliente_router
from project.api.routes.produto import produto_router
from project.api.routes.carrinho import carrinho_router
from project.api.routes.compra import compra_router
from project.api.routes.historico import historico_router

app = FastAPI(title="PROJECT CPDI",)
app.include_router(cliente_router)
app.include_router(produto_router)
app.include_router(carrinho_router)
app.include_router(compra_router)
app.include_router(historico_router)

@app.get("/")
def home():
  return {"mensagem":"isso funciona"}