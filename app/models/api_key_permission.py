from sqlalchemy import Column, Integer, ForeignKey
from app.config.database import Base

class ApiKeyPermission(Base):
    __tablename__ = "api_key_permissions"

    api_key_id = Column(Integer,ForeignKey("api_keys.id") ,primary_key=True, nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id") ,primary_key=True,nullable=False)
