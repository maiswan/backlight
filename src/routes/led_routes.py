from fastapi import APIRouter, Body, status, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from ..config import LedConfig
from .deep_merge import deep_merge

router = APIRouter()

# GET
@router.get("")
async def get(request: Request):
    state = request.state.state
    return state.config.leds

# PATCH
@router.patch("", status_code=status.HTTP_204_NO_CONTENT)
async def patch(request: Request, payload = Body(...)):
    state = request.state.state

    current = state.config.leds.model_dump()
    merged = deep_merge(current, payload)

    try:
        validated = LedConfig.model_validate(merged)
        state.config.leds = validated
        state.config.write()
        
    except ValidationError as e:
        raise RequestValidationError(e.errors()) from e
