from fastapi import FastAPI

from app.core import add
from app.schemas import AddRequest, AddResponse

app = FastAPI()

@app.post("/add", response_model=AddResponse)
def read_root(request: AddRequest) -> AddResponse:
    return AddResponse(result=add(request.a, request.b))