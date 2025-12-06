import asyncio
import copy
import json
from fastapi import APIRouter, Body, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from model.state import state

router = APIRouter()

async def get_stream():
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
async def get_config():
    return state.config.to_dict()

@router.get("/stream")
async def get_config_stream():
    return StreamingResponse(get_stream(), media_type="text/event-stream")


# Payload
class IntPayload(BaseModel):
    value: int = Field(..., ge=0)

class StrPayload(BaseModel):
    value: str

class BoolPayload(BaseModel):
    value: bool

# led_count
@router.get("/led_count")
async def get_led_count():
    return state.config.led_count

@router.put("/led_count", status_code=status.HTTP_204_NO_CONTENT)
async def put_led_count(payload: IntPayload = Body(...)):
    state.config.led_count = payload.value
    state.initialize_pixels()
    state.config.write()

# pixel_order
@router.get("/pixel_order")
async def get_pixel_order():
    return state.config.pixel_order

@router.put("/pixel_order", status_code=status.HTTP_204_NO_CONTENT)
async def put_pixel_order(payload: StrPayload = Body(...)):
    state.config.pixel_order = payload.value
    state.initialize_pixels()
    state.config.write()

# pixel_order
@router.get("/spi_enabled")
async def get_spi_enabled():
    return state.config.pixel_order

@router.put("/spi_enabled", status_code=status.HTTP_204_NO_CONTENT)
async def put_spi_enabled(payload: BoolPayload = Body(...)):
    state.config.spi_enabled = payload.value
    state.initialize_pixels()
    state.config.write()

# pwm_pin
@router.get("/pwm_pin")
async def get_pwm_pin():
    return state.config.pwm_pin

@router.put("/pwm_pin", status_code=status.HTTP_204_NO_CONTENT)
async def put_pwm_pin(payload: IntPayload = Body(...)):
    state.config.pwm_pin = payload.value
    state.initialize_pixels()
    state.config.write()

# pwm_pin
@router.get("/fps")
async def get_fps():
    return state.config.fps

@router.put("/fps", status_code=status.HTTP_204_NO_CONTENT)
async def put_fps(payload: IntPayload = Body(...)):
    state.config.fps = payload.value
    state.config.write()

# fps_static
@router.get("/fps_static")
async def get_fps_static():
    return state.config.fps_static

@router.put("/fps_static", status_code=status.HTTP_204_NO_CONTENT)
async def put_fps_static(payload: IntPayload = Body(...)):
    state.config.fps_static = payload.value
    state.config.write()
