from fastapi import FastAPI
from project.api.routes.cliente import cliente_router
from project.api.routes.produto import produto_router

app = FastAPI(title="PROJECT CPDI",)
app.include_router(cliente_router)
app.include_router(produto_router)

@app.get("/")
def home():
  return {"mensagem":"isso funciona"}