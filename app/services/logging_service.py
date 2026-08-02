from app.models.request_log import RequestLog
from sqlalchemy.orm import Session
from app.repositories.request_log_repository import RequestLogRepository


class LoggingService:
    def __init__(self, request_log_repository: RequestLogRepository):
        self.request_log_repository = request_log_repository

    def log_request(self,user_id,endpoint,method,status_code,ip_address,user_agent,response_time) -> RequestLog:
        request_log = RequestLog(user_id=user_id, endpoint=endpoint, method=method, status_code=status_code)
        return self.request_log_repository.create_request_log(request_log)