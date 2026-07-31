from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.connection import Base


class Project(Base):

    __tablename__ = "projects"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    organization_id = Column(
        Integer,
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False
    )

    name = Column(
        String(150),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    organization = relationship(
        "Organization",
        back_populates="projects"
    )

    tokens = relationship(
        "ApiToken",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    logs = relationship(
        "Log",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    members = relationship(
        "ProjectMember",
        back_populates="project",
        cascade="all, delete-orphan"
    )