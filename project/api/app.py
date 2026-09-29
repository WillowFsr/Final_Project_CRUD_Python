from fastapi import FastAPI
from project.api.routes.cliente import cliente_router

app = FastAPI(title="PROJECT CPDI",)
app.include_router(cliente_router)

@app.get("/")
def home():
  return {"mensagem":"isso funciona"} 