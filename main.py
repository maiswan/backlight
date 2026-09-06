from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src import State, server_router, led_router, renderer_router, command_router, home_router

version = {
    "major": 4,
    "minor": 0,
    "patch": 0,
}
version_major = f"v{version["major"]}"
version_str = f"{version['major']}.{version['minor']}.{version['patch']}"

state = State()

@asynccontextmanager
async def lifespan(_: FastAPI):
    with State() as state:
        yield { "state": state }

app = FastAPI(
    title="LED controller for WS2812B",
    lifespan=lifespan,
    version=version_str
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "PUT", "PATCH", "POST", "DELETE"],
)

app.include_router(server_router, prefix=f"/api/{version_major}/server", tags=["server"])
app.include_router(led_router, prefix=f"/api/{version_major}/leds", tags=["leds"])
app.include_router(renderer_router, prefix=f"/api/{version_major}/renderer", tags=["renderer"])
app.include_router(command_router, prefix=f"/api/{version_major}/commands", tags=["commands"])
app.include_router(home_router, prefix=f"/api/{version_major}", tags=["home"])
app.mount("/dashboard", StaticFiles(directory="dashboard/dist", html=True))

@app.get("/")
async def root():
    return {
        "program": "backlight",
        "author": "maiswan",
        "version": version_str
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=state.config.server.port)
