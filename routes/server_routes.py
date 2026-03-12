from fastapi import APIRouter, Body, status, Request, HTTPException
from pydantic import ValidationError
from model.state import State
from .payloads import IntPayload, ListStrPayload

router = APIRouter()

# port
@router.get("/port")
async def get_port(request: Request):
    state = request.state.state
    return state.config.port

@router.put("/port", status_code=status.HTTP_204_NO_CONTENT)
async def put_led_count(request: Request, payload: IntPayload = Body(...)):
    state = request.state.state
    state.config.port = payload.value
    state.config.write()



# allowed_ips
@router.get("/allowed_ips")
async def get_allowed_ips(request: Request):
    state = request.state.state
    return state.config.port

@router.put("/allowed_ips", status_code=status.HTTP_204_NO_CONTENT)
async def put_allowed_ips(request: Request, payload: ListStrPayload = Body(...)):
    state = request.state.state
    state.config.port = payload.value
    state.config.write()
