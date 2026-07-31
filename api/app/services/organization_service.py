from sqlalchemy.orm import Session

from fastapi import HTTPException

from app.models.organization import Organization
from app.models.enums import UserRole


class OrganizationService:

    @staticmethod
    def create(
        db: Session,
        user,
        data
    ):

        if user.role != UserRole.SUPER_ADMIN:
            raise HTTPException(
                status_code=403,
                detail="Somente administradores podem criar organizações."
            )

        exists = (
            db.query(Organization)
            .filter(
                Organization.slug == data.slug
            )
            .first()
        )

        if exists:
            raise HTTPException(
                status_code=400,
                detail="Slug já utilizado."
            )

        organization = Organization(
            name=data.name,
            slug=data.slug
        )

        db.add(organization)
        db.commit()
        db.refresh(organization)

        return organization

    @staticmethod
    def list(
        db: Session,
        user
    ):

        return (
            db.query(Organization)
            .filter(
                Organization.id == user.organization_id
            )
            .all()
        )

    @staticmethod
    def get(
        db: Session,
        user,
        organization_id: int
    ):

        organization = (
            db.query(Organization)
            .filter(
                Organization.id == organization_id
            )
            .first()
        )

        if not organization:
            raise HTTPException(
                status_code=404,
                detail="Organização não encontrada."
            )

        if organization.id != user.organization_id:
            raise HTTPException(
                status_code=403,
                detail="Sem acesso."
            )

        return organization

    @staticmethod
    def update(
        db: Session,
        user,
        organization_id: int,
        data
    ):

        organization = OrganizationService.get(
            db,
            user,
            organization_id
        )

        organization.name = data.name
        organization.slug = data.slug

        db.commit()
        db.refresh(organization)

        return organization

    @staticmethod
    def delete(
        db: Session,
        user,
        organization_id: int
    ):

        organization = OrganizationService.get(
            db,
            user,
            organization_id
        )

        db.delete(organization)
        db.commit()

        return {
            "message": "Organização removida."
        }