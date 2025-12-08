import asyncio
import copy
import json
from fastapi import APIRouter, Body, status, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from model.state import State

router = APIRouter()

async def get_stream(state: State):
    previous = None
    try:
        while True:
            now = copy.deepcopy(state.config)

            if now != previous:
                previous = now
                yield f"data: {json.dumps(now.to_dict())}\n\n"

            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Exiting stream.")

# GET overview
@router.get("/")
async def get_config(request: Request):
    state = request.state.state
    return state.config.to_dict()

@router.get("/stream")
async def get_config_stream(request: Request):
    state = request.state.state
    return StreamingResponse(get_stream(state), media_type="text/event-stream")


# Payload
class IntPayload(BaseModel):
    value: int = Field(..., ge=0)

class StrPayload(BaseModel):
    value: str

class BoolPayload(BaseModel):
    value: bool

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

# led_count
@router.get("/led_count")
async def get_led_count(request: Request):
    state = request.state.state
    return state.config.led_count

@router.put("/led_count", status_code=status.HTTP_204_NO_CONTENT)
async def put_led_count(request: Request, payload: IntPayload = Body(...)):
    state = request.state.state
    state.config.led_count = payload.value
    state.initialize_pixels()
    state.config.write()

# pixel_order
@router.get("/pixel_order")
async def get_pixel_order(request: Request):
    state = request.state.state
    return state.config.pixel_order

@router.put("/pixel_order", status_code=status.HTTP_204_NO_CONTENT)
async def put_pixel_order(request: Request, payload: StrPayload = Body(...)):
    state = request.state.state
    state.config.pixel_order = payload.value
    state.initialize_pixels()
    state.config.write()

# pixel_order
@router.get("/spi_enabled")
async def get_spi_enabled(request: Request):
    state = request.state.state
    return state.config.pixel_order

@router.put("/spi_enabled", status_code=status.HTTP_204_NO_CONTENT)
async def put_spi_enabled(request: Request, payload: BoolPayload = Body(...)):
    state = request.state.state
    state.config.spi_enabled = payload.value
    state.initialize_pixels()
    state.config.write()

# pwm_pin
@router.get("/pwm_pin")
async def get_pwm_pin(request: Request):
    state = request.state.state
    return state.config.pwm_pin

@router.put("/pwm_pin", status_code=status.HTTP_204_NO_CONTENT)
async def put_pwm_pin(request: Request, payload: IntPayload = Body(...)):
    state = request.state.state
    state.config.pwm_pin = payload.value
    state.initialize_pixels()
    state.config.write()

# pwm_pin
@router.get("/fps")
async def get_fps(request: Request):
    state = request.state.state
    return state.config.fps

@router.put("/fps", status_code=status.HTTP_204_NO_CONTENT)
async def put_fps(request: Request, payload: IntPayload = Body(...)):
    state = request.state.state
    state.config.fps = payload.value
    state.config.write()

# fps_static
@router.get("/fps_static")
async def get_fps_static(request: Request):
    state = request.state.state
    return state.config.fps_static

@router.put("/fps_static", status_code=status.HTTP_204_NO_CONTENT)
async def put_fps_static(request: Request, payload: IntPayload = Body(...)):
    state = request.state.state
    state.config.fps_static = payload.value
    state.config.write()
