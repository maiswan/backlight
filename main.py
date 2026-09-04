# Singleton config
from model.state import State

# HTTP server
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.normalize_path_middleware import NormalizePathMiddleware
from routes.server_routes import router as server_router
from routes.led_routes import router as led_router
from routes.renderer_routes import router as renderer_router
from routes.command_routes import router as command_router
from routes.home_routes import router as home_router

state = State()

@asynccontextmanager
async def lifespan(_: FastAPI):
    with State() as state:
        yield { "state": state }

app = FastAPI(
    title="LED controller for WS2812B",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "PUT", "PATCH", "POST", "DELETE"],
)

app.add_middleware(NormalizePathMiddleware)

version = {
    "major": 4,
    "minor": 0,
    "patch": 0,
}
major = version["major"]

app.include_router(server_router, prefix=f"/api/v{major}/server", tags=["server"])
app.include_router(led_router, prefix=f"/api/v{major}/leds", tags=["leds"])
app.include_router(renderer_router, prefix=f"/api/v{major}/renderer", tags=["renderer"])
app.include_router(command_router, prefix=f"/api/v{major}/commands", tags=["commands"])
app.include_router(home_router, prefix=f"/api/v{major}", tags=["home"])
app.mount("/dashboard", StaticFiles(directory="dashboard/dist", html=True))

@app.get("/")
async def root():
    return {
        "program": "backlight",
        "author": "maiswan",
        "version": f"{version['major']}.{version['minor']}.{version['patch']}"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=state.config.server.port)
