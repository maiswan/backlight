import asyncio
import copy
import json
from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from model.state import state

router = APIRouter()

async def get_stream():
    previous = None
    try:
        while not state.stop_event.is_set():
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

# led_count
@router.get("/led_count")
async def get_led_count():
    return state.config.led_count

@router.put("/led_count")
async def put_led_count(payload: IntPayload = Body(...)):
    state.config.led_count = payload.value
    state.initialize_pixels()
    return {"detail": "changed"}

# pixel_order
@router.get("/pixel_order")
async def get_pixel_order():
    return state.config.pixel_order

@router.put("/pixel_order")
async def put_pixel_order(payload: StrPayload = Body(...)):
    state.config.pixel_order = payload.value
    state.initialize_pixels()
    return {"detail": "changed"}

# gpio_pin
@router.get("/gpio_pin")
async def get_gpio_pin():
    return state.config.gpio_pin

@router.put("/gpio_pin")
async def put_gpio_pin(payload: IntPayload = Body(...)):
    state.config.gpio_pin = payload.value
    state.initialize_pixels()
    return {"detail": "changed"}


# gpio_pin
@router.get("/fps")
async def get_fps():
    return state.config.fps

@router.put("/fps")
async def put_fps(payload: IntPayload = Body(...)):
    state.config.fps = payload.value
    return {"detail": "changed"}