from fastapi import Request
from starlette.responses import Response
from app.services.rate_limit_service import RateLimitService
from app.security.jwt_handler import decode_access_token

async def rate_limit_middleware(request: Request, call_next):
    print("🚦 RATE LIMIT MIDDLEWARE:", request.url.path)    
    userId = None

    authorization = request.headers.get("Authorization")

    if authorization:
        try:
            token = authorization.replace("Bearer ", "")
            userId = decode_access_token(token)
        except Exception:
            userId = None
    
    # Create a unique key for the user or IP address
    key = f"rate_limit:{userId or request.client.host}:{request.url.path}"

    # Initialize the rate limit service
    rate_limit_service = RateLimitService(limit=5, window=60)

    # Check if the request is allowed
    if not rate_limit_service.is_allowed(key):
        return Response(content="Rate limit exceeded", status_code=429)
    
    # Proceed with the request
    response = await call_next(request)
    
    return response


