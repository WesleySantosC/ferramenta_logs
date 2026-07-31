from fastapi import HTTPException

from app.models.project import Project
from app.models.project_member import ProjectMember


class ProjectService:


    @staticmethod
    def create(
        db,
        user,
        data
    ):

        project = Project(
            organization_id=user.organization_id,
            name=data.name,
            description=data.description
        )

        db.add(project)
        db.commit()
        db.refresh(project)

        return project


    @staticmethod
    def list(
        db,
        user
    ):

        # ADMIN vê todos da organização
        if user.role.value == "SUPER_ADMIN":

            return (
                db.query(Project)
                .filter(
                    Project.organization_id == user.organization_id
                )
                .all()
            )


        # MEMBER vê somente projetos vinculados
        return (
            db.query(Project)
            .join(ProjectMember)
            .filter(
                ProjectMember.user_id == user.id
            )
            .all()
        )


    @staticmethod
    def get(
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
                detail="Sem acesso ao projeto"
            )


        return project


    @staticmethod
    def update(
        db,
        project_id,
        data
    ):

        project = (
            db.query(Project)
            .filter(
                Project.id == project_id
            )
            .first()
        )

        if not project:
            raise HTTPException(
                status_code=404,
                detail="Projeto não encontrado"
            )


        if data.name:
            project.name = data.name

        if data.description is not None:
            project.description = data.description

        if data.active is not None:
            project.active = data.active


        db.commit()
        db.refresh(project)

        return project


    @staticmethod
    def delete(
        db,
        project_id
    ):

        project = (
            db.query(Project)
            .filter(
                Project.id == project_id
            )
            .first()
        )


        if not project:
            raise HTTPException(
                status_code=404,
                detail="Projeto não encontrado"
            )


        db.delete(project)
        db.commit()


        return {
            "message": "Projeto removido"
        }