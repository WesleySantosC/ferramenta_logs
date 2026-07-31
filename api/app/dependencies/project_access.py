from fastapi import HTTPException

from app.models.project import Project
from app.models.project_member import ProjectMember


def verify_project_access(
    db,
    user,
    project_id
):

    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.organization_id == user.organization_id
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Projeto não encontrado"
        )

    if user.role.value == "SUPER_ADMIN":
        return project

    member = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user.id
        )
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=403,
            detail="Usuário sem acesso ao projeto"
        )

    return project