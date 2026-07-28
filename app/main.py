
import structlog
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette.templating import _TemplateResponse

from app.config import settings
from app.core import add
from app.logging_config import configure_logging
from app.schemas import AddRequest, AddResponse

configure_logging()
logger = structlog.get_logger()

limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])

app = FastAPI(title=settings.app_name)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) # type: ignore[arg-type]  # slowapi/starlette type-stub mismatch, see laurentS/slowapi#188
app.add_middleware(SlowAPIMiddleware)

templates = Jinja2Templates(directory="app/templates")

@app.post("/add", response_model=AddResponse)
async def read_root(request: AddRequest) -> AddResponse:
    result = add(request.a, request.b)
    logger.info("api_add", a=request.a, b=request.b, result=result)
    return AddResponse(result=result)

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/")
async def read_index(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse(request=request, name="index.html", context={})

@app.post("/add-form", response_class=HTMLResponse)
async def add_form(request: Request, a: float = Form(...), b: float = Form(...)) -> HTMLResponse:
    result = add(a, b)
    logger.info("form_add", a=a, b=b, result=result)
    return templates.TemplateResponse(
        request=request, name="result.html", context={"result": result}
        )