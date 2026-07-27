from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

from app.core import add
from app.schemas import AddRequest, AddResponse

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.post("/add", response_model=AddResponse)
def read_root(request: AddRequest) -> AddResponse:
    return AddResponse(result=add(request.a, request.b))

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/")
def read_index(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse(request=request, name="index.html", context={})