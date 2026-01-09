import asyncio
import copy
import json
from fastapi import APIRouter, Body, status, Request, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, ValidationError
from model.state import State

router = APIRouter()

async def get_stream(state: State):
    previous = None
    try:
        while True:
            now = copy.deepcopy(state.config)

            if now != previous:
                previous = now
                dump = state.config.model_dump_json()
                yield f"data: {dump}\n\n"

            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Exiting stream.")

# GET overview
@router.get("/")
async def get_config(request: Request):
    state = request.state.state
    return state.config.model_dump(mode='json')

@router.get("/stream")
async def get_config_stream(request: Request):
    state = request.state.state
    return StreamingResponse(get_stream(state), media_type="text/event-stream")
