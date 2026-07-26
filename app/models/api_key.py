from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.config.database import Base

class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)

    key_hash = Column(String(255), unique=True, index=True, nullable=False)

    user_id = Column(Integer, nullable=False)

    name = Column(String(100), nullable=False)

    active = Column(bool, nullable=False, default=True)

    expiry_date = Column(DateTime(timezone=True), nullable=True)

    last_used_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
