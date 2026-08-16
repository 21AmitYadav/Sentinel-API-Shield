import time

from fastapi import Request
from starlette.responses import Response

from app.config.database import SessionLocal
from app.repositories.request_log_repository import RequestLogRepository
from app.security.jwt_handler import decode_access_token
from app.services.logging_service import LoggingService


async def logging_middleware(request: Request, call_next):

    # 1. Start timer
    print("🔥 MIDDLEWARE RUNNING:", request.method, request.url.path)

    start_time = time.time()

    # 2. Default values
    user_id = None
    response = None
    status_code = 500

    # 3. Decode JWT (if present)
    authorization = request.headers.get("Authorization")

    if authorization:
        try:
            token = authorization.replace("Bearer ", "")
            user_id = decode_access_token(token)
        except Exception:
            user_id = None

    # 4. Execute the endpoint
    try:
        response = await call_next(request)
        status_code = response.status_code

    except Exception:
        status_code = 500
        raise

    finally:

        # 5. Calculate response time
        process_time = (time.time() - start_time) * 1000

        # 6. Create DB session
        db = SessionLocal()

        try:
            repository = RequestLogRepository(db)
            service = LoggingService(repository)

            service.log_request(
                user_id=user_id,
                endpoint=request.url.path,
                method=request.method,
                status_code=status_code,
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("User-Agent"),
                response_time=process_time,
            )

        except Exception as e:
            print("❌ REQUEST LOGGING ERROR:", repr(e))     
            
            pass

        finally:
            db.close()

    return response