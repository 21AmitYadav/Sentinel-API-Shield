from app.services.rate_limit_service import RateLimitService
from app.config.redis import redis_client


redis_client.delete("test:rate:user:1")

service = RateLimitService(
    limit=5,
    window=60
)

for i in range(1, 8):

    allowed = service.is_allowed("test:rate:user:1")

    print(
        f"Request {i}:",
        "ALLOWED" if allowed else "BLOCKED"
    )