from app.dependencies.permissions import require_admin
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal

from app.dependencies.auth import get_current_user

from app.services.organization_service import OrganizationService

from app.schemas.organization import (
    OrganizationCreateSchema,
    OrganizationUpdateSchema,
    OrganizationResponseSchema
)

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post(
    "",
    response_model=OrganizationResponseSchema
)
def create(
    data: OrganizationCreateSchema,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    return OrganizationService.create(
        db,
        user,
        data
    )


@router.get(
    "",
    response_model=list[OrganizationResponseSchema]
)
def list_all(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    return OrganizationService.list(
        db,
        user
    )


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponseSchema
)
def get(
    organization_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    return OrganizationService.get(
        db,
        user,
        organization_id
    )


@router.put(
    "/{organization_id}",
    response_model=OrganizationResponseSchema
)
def update(
    organization_id: int,
    data: OrganizationUpdateSchema,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    return OrganizationService.update(
        db,
        user,
        organization_id,
        data
    )


@router.delete(
    "/{organization_id}"
)
def delete(
    organization_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_admin)
):

    return OrganizationService.delete(
        db,
        user,
        organization_id
    )