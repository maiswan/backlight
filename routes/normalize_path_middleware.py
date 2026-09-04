from fastapi import FastAPI, APIRouter
from starlette.types import ASGIApp, Receive, Scope, Send

class NormalizePathMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):

        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        if scope["path"].lower() == "/openapi.json":
            return await self.app(scope, receive, send)

        # Enforce trailing "/"
        if not scope["path"].endswith("/"):
            scope["path"] += "/"
                
        await self.app(scope, receive, send)
