from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func

from app.database.connection import Base


class Log(Base):

    __tablename__ = "logs"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    application = Column(
        String(100),
        nullable=False
    )

    service = Column(
        String(100),
        nullable=False
    )

    level = Column(
        String(20),
        nullable=False
    )

    message = Column(
        Text,
        nullable=False
    )

    environment = Column(
        String(50),
        nullable=False
    )

    request_id = Column(
        String(100),
        nullable=True
    )

    context = Column(
        JSON,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )