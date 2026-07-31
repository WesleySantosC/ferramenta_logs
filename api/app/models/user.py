from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.connection import Base
from app.models.enums import UserRole


class User(Base):

    __tablename__ = "users"

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

    email = Column(
        String(200),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    role = Column(
        Enum(UserRole),
        nullable=False,
        default=UserRole.MEMBER
    )

    active = Column(
        Boolean,
        nullable=False,
        default=True
    )

    must_change_password = Column(
        Boolean,
        nullable=False,
        default=True
    )

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

    organization = relationship(
        "Organization",
        back_populates="users"
    )

    projects = relationship(
        "ProjectMember",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<User(id={self.id}, "
            f"name='{self.name}', "
            f"email='{self.email}', "
            f"role='{self.role.value}')>"
        )