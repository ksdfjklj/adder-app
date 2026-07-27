from pydantic import BaseModel, Field


class AddRequest(BaseModel):
    a: float = Field(..., description="The first number to add")
    b: float = Field(..., description="The second number to add")

class AddResponse(BaseModel):
    result: float = Field(..., description="The sum of the two numbers")