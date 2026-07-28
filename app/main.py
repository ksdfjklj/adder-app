import logging

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

from app.config import settings
from app.core import add
from app.schemas import AddRequest, AddResponse

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name)
templates = Jinja2Templates(directory="app/templates")

@app.post("/add", response_model=AddResponse)
def read_root(request: AddRequest) -> AddResponse:
    logger.info(f"API add: {request.a} and {request.b}")
    return AddResponse(result=add(request.a, request.b))

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/")
def read_index(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse(request=request, name="index.html", context={})

@app.post("/add-form", response_class=HTMLResponse)
def add_form(request: Request, a: float = Form(...), b: float = Form(...)) -> HTMLResponse:
    result = add(a, b)
    logger.info(f"Form add: {a} and {b}, result: {result}")
    return templates.TemplateResponse(
        request=request, name="result.html", context={"result": result}
        )