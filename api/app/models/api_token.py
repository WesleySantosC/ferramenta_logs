from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

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


    project_id = Column(
        Integer,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )


    active = Column(
        Boolean,
        default=True,
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    project = relationship(
        "Project",
        back_populates="tokens"
    )