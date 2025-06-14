# Singleton config
from model.state import state

# HTTP server
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.state_routes import router as state_router
from routes.instruction_routes import router as instruction_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # actions on exit
    yield
    await state.deconstruct()

app = FastAPI(
    title="Backlight HTTP endpoint",
    description="Control WS2812B LED strip",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE"],
    allow_headers=["*"],
)

app.include_router(state_router, prefix="/state", tags=["state"])
app.include_router(instruction_router, prefix="/instructions", tags=["instructions"])

app.mount("/dash", StaticFiles(directory="dash/dist", html=True))



