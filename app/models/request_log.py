from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func

from app.config.database import Base

class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=True)

    api_key_id = Column(Integer, nullable=True)

    endpoint = Column(String(255), nullable=False)

    method = Column(String(10), nullable=False)

    status_code = Column(Integer, nullable=False)

    ip_address = Column(String(45), nullable=False)

    user_agent = Column(String(255), nullable=True)

    response_time_ms = Column(Float, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )