# Singleton config
from model.state import State

# HTTP server
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from guard.middleware import SecurityMiddleware
from guard.models import SecurityConfig
from routes.server_routes import router as server_router
from routes.led_routes import router as led_router
from routes.renderer_routes import router as renderer_router
from routes.command_routes import router as command_router
from routes.home_routes import router as home_router

state = State()

@asynccontextmanager
async def lifespan(app: FastAPI):
    state.initialize_output()
    yield { "state": state }

    # actions on exit
    state.deconstruct()

app = FastAPI(
    title="LED controller for WS2812B",
    lifespan=lifespan,
)

config = SecurityConfig(
    whitelist=state.config.server.whitelist,
    enable_cors=True,
    allow_origins=["*"],
    allow_methods=["GET", "PUT", "POST", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(SecurityMiddleware, config=config)

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
        "version": f"{version["major"]}.{version["minor"]}.{version["patch"]}"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=state.config.server.port)
