from jose import jwt, ExpiredSignatureError, JWTError
from fastapi import Request, HTTPException
from core.config import settings


async def auth_required(request: Request) -> int:
    token = request.cookies.get("access")
    if not token:
        raise HTTPException(status_code=401, detail={
            "message": "Access token is missing"
        })
    try:
        jwt_payload = jwt.decode(token, settings.SECRET, algorithms=['HS256'])
        user_id = jwt_payload["sub"]
        if not user_id:
            raise HTTPException(status_code=401, detail={
                "message": "User ID is missing"
            })
        return int(jwt_payload.get("sub"))

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail={
            "message": "Access token is expired"
        })
    except JWTError:
        raise HTTPException(status_code=401, detail={
            "message": "Invalid token"
        })
