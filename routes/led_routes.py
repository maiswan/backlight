import asyncio
import copy
import json
from fastapi import APIRouter, Body, status, Request, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, ValidationError
from model.state import State
from .payloads import IntPayload, StrPayload

router = APIRouter()

# count
@router.get("/count")
async def get_count(request: Request):
    state = request.state.state
    return state.config.leds.count

@router.put("/count", status_code=status.HTTP_204_NO_CONTENT)
async def put_count(request: Request, payload: IntPayload = Body(...)):
    state = request.state.state
    try:
        state.config.leds.count = payload.value
        state.initialize_pixels()
        state.config.write()
    except ValidationError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error))


# pixel_order
@router.get("/pixel_order")
async def get_pixel_order(request: Request):
    state = request.state.state
    return state.config.leds.pixel_order

@router.put("/pixel_order", status_code=status.HTTP_204_NO_CONTENT)
async def put_pixel_order(request: Request, payload: StrPayload = Body(...)):
    state = request.state.state
    try:
        state.config.leds.pixel_order = payload.value
        state.initialize_pixels()
        state.config.write()
    except ValidationError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error))

# transport/mode
@router.get("/transport/mode")
async def get_transport_mode(request: Request):
    state = request.state.state
    return state.config.leds.transport.mode

@router.put("/transport/mode", status_code=status.HTTP_204_NO_CONTENT)
async def put_transport_mode(request: Request, payload: StrPayload = Body(...)):
    state = request.state.state
    try:
        state.config.leds.transport.mode = payload.value
        state.initialize_pixels()
        state.config.write()
    except ValidationError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error))

# transport/pwm/pin
@router.get("/transport/pwm/pin")
async def get_transport_pwm_pin(request: Request):
    state = request.state.state
    return state.config.leds.transport.pwm.pin

@router.put("/transport/pwm/pin", status_code=status.HTTP_204_NO_CONTENT)
async def put_transport_pwm_pin(request: Request, payload: IntPayload = Body(...)):
    state = request.state.state
    try:
        state.config.leds.transport.pwm.pin = payload.value
        state.initialize_pixels()
        state.config.write()
    except ValidationError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error))
