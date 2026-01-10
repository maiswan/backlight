from fastapi import APIRouter, Body, status, Request, HTTPException
from pydantic import ValidationError
from model.state import State
from model.renderer.transitioner import EasingMode
from .payloads import FloatPayload, StrPayload

router = APIRouter()

# framerate/active
@router.get("/framerate/active")
async def get_framerate_active(request: Request):
    state = request.state.state
    return state.config.renderer.framerate.active

@router.put("/framerate/active", status_code=status.HTTP_204_NO_CONTENT)
async def pyt_framerate_active(request: Request, payload: FloatPayload = Body(...)):
    state = request.state.state
    try:
        state.config.renderer.framerate.active = payload.value
        state.config.write()
        state.initialize_render_task()
    except ValidationError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error))

# framerate/idle
@router.get("/framerate/idle")
async def get_fps_static(request: Request):
    state = request.state.state
    return state.config.renderer.framerate.idle

@router.put("/framerate/idle", status_code=status.HTTP_204_NO_CONTENT)
async def put_fps_static(request: Request, payload: FloatPayload = Body(...)):
    state = request.state.state
    try:
        state.config.renderer.framerate.idle = payload.value
        state.config.write()
        state.initialize_render_task()
    except ValidationError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error))


# transitions/duration
@router.get("/transitions/duration")
async def get_transitions_duration(request: Request):
    state = request.state.state
    return state.config.renderer.transitions.duration

@router.put("/transitions/duration", status_code=status.HTTP_204_NO_CONTENT)
async def put_transitions_duration(request: Request, payload: FloatPayload = Body(...)):
    state = request.state.state
    try:
        state.config.renderer.transitions.duration = payload.value
        state.config.write()
        state.initialize_render_task()
    except ValidationError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error))

# transitions/mode
@router.get("/transitions/mode")
async def get_transitions_duration(request: Request):
    state = request.state.state
    return state.config.renderer.transitions.mode

@router.put("/transitions/mode", status_code=status.HTTP_204_NO_CONTENT)
async def put_transitions_duration(request: Request, payload: StrPayload = Body(...)):
    state = request.state.state
    try:
        state.config.renderer.transitions.mode = EasingMode(payload.value)
        state.config.write()
        state.initialize_render_task()
    except ValidationError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error))

