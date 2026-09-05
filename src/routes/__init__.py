from .command_routes import router as command_router
from .home_routes import router as home_router
from .led_routes import router as led_router
from .renderer_routes import router as renderer_router
from .server_routes import router as server_router

__all__ = [
    "command_router",
    "home_router",
    "led_router",
    "renderer_router",
    "server_router",
]