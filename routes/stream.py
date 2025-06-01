import asyncio
import copy
import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from model.state import state

router = APIRouter()

async def stream():
    previous = None
    try:
        while not state.stop_sse_event.is_set():
            now = copy.deepcopy(state.config)

            if now != previous:
                previous = now
                yield f"data: {json.dumps(now.to_dict())}\n\n"

            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Exiting.")

# GETs
@router.get("/")
async def get_stream():
    return StreamingResponse(stream(), media_type="text/event-stream")