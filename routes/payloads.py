from pydantic import BaseModel

class IntPayload(BaseModel):
    value: int

class FloatPayload(BaseModel):
    value: float

class StrPayload(BaseModel):
    value: str
