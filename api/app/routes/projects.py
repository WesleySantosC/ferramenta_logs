from fastapi import APIRouter, Depends

from app.database.connection import SessionLocal

from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_admin

from app.schemas.project import (
    ProjectCreateSchema,
    ProjectUpdateSchema
)

from app.services.project_service import ProjectService


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



@router.post("/")
def create_project(
    data: ProjectCreateSchema,
    user = Depends(require_admin),
    db = Depends(get_db)
):

    return ProjectService.create(
        db,
        user,
        data
    )



@router.get("/")
def list_projects(
    user = Depends(get_current_user),
    db = Depends(get_db)
):

    return ProjectService.list(
        db,
        user
    )



@router.get("/{project_id}")
def get_project(
    project_id:int,
    user = Depends(get_current_user),
    db = Depends(get_db)
):

    return ProjectService.get(
        db,
        user,
        project_id
    )



@router.put("/{project_id}")
def update_project(
    project_id:int,
    data:ProjectUpdateSchema,
    user = Depends(require_admin),
    db = Depends(get_db)
):

    return ProjectService.update(
        db,
        project_id,
        data
    )



@router.delete("/{project_id}")
def delete_project(
    project_id:int,
    user = Depends(require_admin),
    db = Depends(get_db)
):

    return ProjectService.delete(
        db,
        project_id
    )