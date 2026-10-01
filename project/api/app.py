from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from project.api.routes.carrinho import carrinho_router
from project.api.routes.cliente import cliente_router
from project.api.routes.compra import compra_router
from project.api.routes.historico import historico_router
from project.api.routes.produto import produto_router

API_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = API_DIR / "templates"
PAGES_DIR = TEMPLATES_DIR / "pages"
STATIC_DIR = TEMPLATES_DIR / "static"

templates = Jinja2Templates(directory=str(PAGES_DIR))

app = FastAPI(title="Aurea — Loja Online")

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

app.include_router(cliente_router)
app.include_router(carrinho_router)
app.include_router(compra_router)
app.include_router(historico_router)
app.include_router(produto_router)


def render_page(request: Request, name: str, titulo: str):
  return templates.TemplateResponse(
    request=request,
    name=name,
    context={"titulo": titulo},
  )


@app.get("/", include_in_schema=False)
def home(request: Request):
  return render_page(request, "index.html", "Aurea — Loja online")


@app.get("/loja", include_in_schema=False)
def loja(request: Request):
  return render_page(request, "loja.html", "Loja — Aurea")


@app.get("/conta", include_in_schema=False)
def conta(request: Request):
  return render_page(request, "conta.html", "Minha conta — Aurea")


@app.get("/sacola", include_in_schema=False)
def sacola(request: Request):
  return render_page(request, "sacola.html", "Sacola — Aurea")


@app.get("/checkout", include_in_schema=False)
def checkout(request: Request):
  return render_page(request, "checkout.html", "Checkout — Aurea")


@app.get("/historico", include_in_schema=False)
def historico(request: Request):
  return render_page(request, "historico.html", "Histórico — Aurea")


@app.get("/gestao", include_in_schema=False)
def gestao(request: Request):
  return render_page(request, "gestao.html", "Gestão de produtos — Aurea")
