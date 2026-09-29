from fastapi import FastAPI

app = FastAPI(title="PROJECT CPDI")

@app.get("/")
def home():
  return {"mensagem":"isso funciona"}