from fastapi import FastAPI

from app.core import add

app = FastAPI()

@app.post("/add")
def read_root(a: float, b: float) -> dict[str, float]:
    return {"result": add(a, b)}