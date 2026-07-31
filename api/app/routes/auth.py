from app.dependencies.auth import get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    return AuthService.login(
        db=db,
        data=data
    )

@router.post(
    "/register"
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    return AuthService.register(
        db=db,
        data=data
    )

@router.get(
    "/me",
    summary="Retorna o usuário autenticado"
)
def me(
    user = Depends(get_current_user)
):

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "organization_id": user.organization_id,
        "role": user.role.value
    }


@router.post(
    "/logout",
    summary="Efetua logout"
)
def logout():
    return {
        "message": "Logout realizado com sucesso."
    }