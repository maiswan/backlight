import asyncio
import copy
import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
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

# GET
@router.get("/")
async def get_state(stream: bool = False):
    if (stream):
        return StreamingResponse(get_stream(), media_type="text/event-stream")
    
    return state.to_dict()