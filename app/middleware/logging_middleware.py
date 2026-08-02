from fastapi import Request, Response
import time
from app.security.jwt_handler import decode_access_token
from app.services.logging_service import LoggingService
from app.repositories.request_log_repository import RequestLogRepository
from app.config.database import SessionLocal

async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    response: Response = await call_next(request)
    process_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    authorization = request.headers.get("Authorization")

    if authorization:
        try:
            token = authorization.replace("Bearer ", "")
            user_id = decode_access_token(token)
        except:
            user_id = None
    else:
        user_id = None    
    db = SessionLocal()
    RequestLogRepository_instance = RequestLogRepository(db)
    logging_service = LoggingService(RequestLogRepository_instance)
    try:
        logging_service.log_request(user_id=user_id, endpoint=request.url.path, method=request.method, status_code=response.status_code, ip_address=request.client.host, user_agent=request.headers.get("user-agent"), response_time=process_time)
    except Exception:
        # Log internally if needed, but don't break the request
        pass
    