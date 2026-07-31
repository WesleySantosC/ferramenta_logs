from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.connection import Base


class Organization(Base):

    __tablename__ = "organizations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(150),
        nullable=False
    )

    slug = Column(
        String(150),
        unique=True,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    users = relationship(
        "User",
        back_populates="organization",
        cascade="all, delete-orphan"
    )

    projects = relationship(
        "Project",
        back_populates="organization",
        cascade="all, delete-orphan"
    )