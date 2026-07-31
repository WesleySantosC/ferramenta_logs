from fastapi import Depends, HTTPException

from app.dependencies.auth import get_current_user
from app.models.enums import UserRole


def require_admin(
    current_user=Depends(get_current_user)
):
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Apenas administradores podem realizar esta operação."
        )

    return current_user


def require_member(
    current_user=Depends(get_current_user)
):
    return current_user