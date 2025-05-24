from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from starlette.responses import JSONResponse

from core.config import settings


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        x_api_key = settings.X_API_KEY
        key_from_header = request.headers.get("X-API-KEY")

        if not key_from_header and x_api_key != key_from_header:
            return JSONResponse(
                {
                    "error": "X-API-KEY header missing.",
                }, status_code=401
            )

        return await call_next(request)
