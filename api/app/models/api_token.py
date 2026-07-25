from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from app.database.connection import Base


class ApiToken(Base):

    __tablename__ = "api_tokens"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    token = Column(
        String(255),
        unique=True,
        nullable=False
    )

    application = Column(
        String(100),
        nullable=False
    )

    active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )