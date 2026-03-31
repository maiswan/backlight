from fastapi import APIRouter, Body, status, Request, HTTPException
from pydantic import ValidationError
from model.state import State
from .payloads import IntPayload, StrPayload, ListStrPayload

router = APIRouter()

# port
@router.get("/port")
async def get_port(request: Request):
    config = request.state.state.config
    return config.server.port

@router.put("/port", status_code=status.HTTP_204_NO_CONTENT)
async def put_led_count(request: Request, payload: IntPayload = Body(...)):
    config = request.state.state.config
    config.server.port = payload.value
    config.write()



# whitelist
@router.get("/whitelist")
async def get_whitelist(request: Request):
    config = request.state.state.config
    return config.server.whitelist

@router.put("/whitelist", status_code=status.HTTP_204_NO_CONTENT)
async def put_whitelist(request: Request, payload: ListStrPayload = Body(...)):
    config = request.state.state.config
    config.server.whitelist = payload.value
    config.write()

@router.post("/whitelist", status_code=status.HTTP_204_NO_CONTENT)
async def post_whitelist(request: Request, payload: StrPayload = Body(...)):
    config = request.state.state.config
    config.server.whitelist.append(payload.value)
    config.write()

@router.delete("/whitelist/{ip}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_whitelist(request: Request, ip: str):
    config = request.state.state.config
    config.server.whitelist = [ x for x in config.server.whitelist if not x == ip ]
    config.write()



# blacklist
@router.get("/blacklist")
async def get_blacklist(request: Request):
    config = request.state.state.config
    return config.server.blacklist

@router.put("/blacklist", status_code=status.HTTP_204_NO_CONTENT)
async def put_blacklist(request: Request, payload: ListStrPayload = Body(...)):
    config = request.state.state.config
    config.server.blacklist = payload.value
    config.write()

@router.post("/blacklist", status_code=status.HTTP_204_NO_CONTENT)
async def post_blacklist(request: Request, payload: StrPayload = Body(...)):
    config = request.state.state.config
    config.server.blacklist.append(payload.value)
    config.write()

@router.delete("/blacklist/{ip}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blacklist(request: Request, ip: str):
    config = request.state.state.config
    config.server.blacklist = [ x for x in config.server.blacklist if not x == ip ]
    config.write()
