
import structlog
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

from app.config import settings
from app.core import add
from app.logging_config import configure_logging
from app.schemas import AddRequest, AddResponse

configure_logging()
logger = structlog.get_logger()

app = FastAPI(title=settings.app_name)
templates = Jinja2Templates(directory="app/templates")

@app.post("/add", response_model=AddResponse)
def read_root(request: AddRequest) -> AddResponse:
    result = add(request.a, request.b)
    logger.info("api_add", a=request.a, b=request.b, result=result)
    return AddResponse(result=result)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/")
def read_index(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse(request=request, name="index.html", context={})

@app.post("/add-form", response_class=HTMLResponse)
def add_form(request: Request, a: float = Form(...), b: float = Form(...)) -> HTMLResponse:
    result = add(a, b)
    logger.info("form_add", a=a, b=b, result=result)
    return templates.TemplateResponse(
        request=request, name="result.html", context={"result": result}
        )