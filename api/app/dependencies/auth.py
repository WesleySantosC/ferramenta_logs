from fastapi import Header, HTTPException
from app.database.connection import SessionLocal
from app.models.api_token import ApiToken
from app.utils.crypto import hash_token


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

    token_hash = hash_token(plain_token)

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