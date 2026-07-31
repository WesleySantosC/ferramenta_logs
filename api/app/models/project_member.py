from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.connection import Base


class ProjectMember(Base):

    __tablename__ = "project_members"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    role = Column(
        String(50),
        default="MEMBER"
    )


    project = relationship(
        "Project",
        back_populates="members"
    )

    user = relationship(
        "User",
        back_populates="projects"
    )