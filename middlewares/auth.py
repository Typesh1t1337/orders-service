from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from core.config import settings

allowed_paths = ["/docs", "/openapi.json", "/redoc"]


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        x_api_key = settings.X_API_KEY
        key_from_header = request.headers.get("X-API-KEY")
        if request.url.path not in allowed_paths and x_api_key != key_from_header:
            raise HTTPException(
                detail={
                    "error": "X-API-KEY header missing.",
                }, status_code=401
            )

        return await call_next(request)
