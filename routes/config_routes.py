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

@router.put("/led_count", status_code=status.HTTP_204_NO_CONTENT)
async def put_led_count(payload: IntPayload = Body(...)):
    state.config.led_count = payload.value
    state.initialize_pixels()
    state.write_config()

# pixel_order
@router.get("/pixel_order")
async def get_pixel_order():
    return state.config.pixel_order

@router.put("/pixel_order", status_code=status.HTTP_204_NO_CONTENT)
async def put_pixel_order(payload: StrPayload = Body(...)):
    state.config.pixel_order = payload.value
    state.initialize_pixels()
    state.write_config()

# gpio_pin
@router.get("/gpio_pin")
async def get_gpio_pin():
    return state.config.gpio_pin

@router.put("/gpio_pin", status_code=status.HTTP_204_NO_CONTENT)
async def put_gpio_pin(payload: IntPayload = Body(...)):
    state.config.gpio_pin = payload.value
    state.initialize_pixels()
    state.write_config()


# gpio_pin
@router.get("/fps")
async def get_fps():
    return state.config.fps

@router.put("/fps", status_code=status.HTTP_204_NO_CONTENT)
async def put_fps(payload: IntPayload = Body(...)):
    state.config.fps = payload.value
    state.write_config()

# fps_all_static_commands
@router.get("/fps_all_static_commands")
async def get_fps_all_static_commands():
    return state.config.fps_all_static_commands

@router.put("/fps_all_static_commands", status_code=status.HTTP_204_NO_CONTENT)
async def put_fps_all_static_commands(payload: IntPayload = Body(...)):
    state.config.fps_all_static_commands = payload.value
    state.write_config()

# force_rerender_gpio_pin
@router.get("/force_rerender_gpio_pin")
async def get_force_rerender_gpio_pin():
    return state.config.force_rerender_gpio_pin

@router.put("/force_rerender_gpio_pin", status_code=status.HTTP_204_NO_CONTENT)
async def put_force_rerender_gpio_pin(payload: IntPayload = Body(...)):
    state.config.force_rerender_gpio_pin = payload.value
    state.write_config()
    state.initialize_force_render_task()