from fastapi import APIRouter, Body, status, Request, HTTPException
from pydantic import ValidationError
from model.state import State
from .payloads import IntPayload

router = APIRouter()

# port
@router.get("/port")
async def get_port(request: Request):
    state = request.state.state
    return state.config.port

@router.put("/port", status_code=status.HTTP_204_NO_CONTENT)
async def put_led_count(request: Request, payload: IntPayload = Body(...)):
    state = request.state.state
    try:
        state.config.port = payload.value
        state.config.write()
    except ValidationError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error))
