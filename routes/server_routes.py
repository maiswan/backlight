from fastapi import APIRouter, Body, status, Request, HTTPException
from pydantic import ValidationError
from model.state import State
from .payloads import IntPayload, ListStrPayload

router = APIRouter()

# port
@router.get("/port")
async def get_port(request: Request):
    state = request.state.state
    return state.config.server.port

@router.put("/port", status_code=status.HTTP_204_NO_CONTENT)
async def put_led_count(request: Request, payload: IntPayload = Body(...)):
    state = request.state.state
    state.config.server.port = payload.value
    state.config.write()



# whitelist
@router.get("/whitelist")
async def get_whitelist(request: Request):
    state = request.state.state
    return state.config.server.whitelist

@router.put("/whitelist", status_code=status.HTTP_204_NO_CONTENT)
async def put_whitelist(request: Request, payload: ListStrPayload = Body(...)):
    state = request.state.state
    state.config.server.whitelist = payload.value
    state.config.write()



# blacklist
@router.get("/blacklist")
async def get_blacklist(request: Request):
    state = request.state.state
    return state.config.server.blacklist

@router.put("/blacklist", status_code=status.HTTP_204_NO_CONTENT)
async def put_blacklist(request: Request, payload: ListStrPayload = Body(...)):
    state = request.state.state
    state.config.server.blacklist = payload.value
    state.config.write()
