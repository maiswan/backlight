# Singleton config
import json

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from model.state import state

# HTTP server
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.color import router as color_router
from routes.alpha import router as alpha_router
from routes.gamma import router as gamma_router
from routes.stream import router as stream_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # actions on startup
    if (state.config.alpha_instruction):
        await state.execute_instruction(state.config.alpha_instruction)
    if (state.config.color_instruction):
        await state.execute_instruction(state.config.color_instruction)
    if (state.config.gamma_instruction):
        await state.execute_instruction(state.config.gamma_instruction)
    state.pixels.brightness = 1.0
        
    yield 
    # actions on exit
    state.stop_sse_event.set()
    # state.pixels.brightness = 0.0
    state.pixels.show()
    with open('config.json', 'w') as f:
        json.dump(state.config.to_dict(), f, indent=4)

app = FastAPI(
    title="Backlight HTTP endpoint",
    description="Control WS2812B LED strip",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "PUT"],
    allow_headers=["*"],
)

app.include_router(color_router, prefix="/color", tags=["color"])
app.include_router(alpha_router, prefix="/alpha", tags=["alpha"])
app.include_router(gamma_router, prefix="/gamma", tags=["gamma"])
app.include_router(stream_router, prefix="/stream", tags=["stream"])

@app.get("/state")
def get_state():
    return state.to_dict()

app.mount("/dash", StaticFiles(directory="dash/dist", html=True))



