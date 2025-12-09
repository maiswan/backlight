# Singleton config
from model.state import State

# HTTP server
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.config_routes import router as config_router
from routes.command_routes import router as command_router

state = State()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    yield { "state": state }
    
    # actions on exit
    await state.deconstruct()

app = FastAPI(
    title="Backlight HTTP endpoint",
    description="Control WS2812B LED strip",
    lifespan=lifespan,
)

app.include_router(config_router, prefix="/api/v3/config", tags=["config"])
app.include_router(command_router, prefix="/api/v3/commands", tags=["commands"])
app.mount("/dashboard", StaticFiles(directory="dashboard/dist", html=True))

@app.get("/")
async def root():
    return "maiswan/backlight"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=state.config.port)
