from app.models.enums import UserRole
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.api_token import ApiToken
from app.models.user import User

from app.utils.crypto import hash_token
from app.utils.jwt import decode_access_token


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

def verify_token(
    authorization: str = Header(...)
):

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    plain_token = authorization.replace(
        "Bearer ",
        ""
    )

    token_hash = hash_token(
        plain_token
    )

    db = SessionLocal()

    try:
        api_token = (
            db.query(ApiToken)
            .filter(
                ApiToken.token == token_hash,
                ApiToken.active == True
            )
            .first()
        )


        if not api_token:
            raise HTTPException(
                status_code=401,
                detail="Token não autorizado"
            )


        return api_token


    finally:
        db.close()

def get_current_user(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="JWT inválido"
        )

    token = authorization.replace(
        "Bearer ",
        ""
    )

    payload = decode_access_token(
        token
    )

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="JWT expirado ou inválido"
        )

    user_id = payload.get(
        "sub"
    )


    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Usuário inválido"
        )

    user = (
        db.query(User)
        .filter(
            User.id == int(user_id)
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado"
        )

    if not user.active:
        raise HTTPException(
            status_code=403,
            detail="Usuário desativado"
        )

    return user