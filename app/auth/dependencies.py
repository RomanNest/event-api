from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from app.auth.jwt_utils import decode_access_token

api_key_header = APIKeyHeader(name="Authorization")


async def get_current_user_id(token: str = Security(api_key_header)) -> int:
    if not token.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid or missing token")

    actual_token = token.removeprefix("Bearer ").strip()
    try:
        payload = decode_access_token(actual_token)
        return int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
