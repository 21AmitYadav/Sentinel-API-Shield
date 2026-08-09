from app.config.redis import redis_client


class RateLimitService:

    def __init__(self, limit: int = 5, window: int = 60):
        self.limit = limit
        self.window = window

    def is_allowed(self, key: str) -> bool:

        count = redis_client.incr(key)

        if count == 1:
            redis_client.expire(key, self.window)

        return count <= self.limit