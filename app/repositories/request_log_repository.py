from app.models.request_log import RequestLog
from sqlalchemy.orm import Session


class RequestLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_request_log(self, request_log: RequestLog) -> RequestLog:
        self.db.add(request_log)
        self.db.commit()
        self.db.refresh(request_log)
        return request_log