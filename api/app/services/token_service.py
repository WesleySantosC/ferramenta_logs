from app.database.connection import SessionLocal
from app.models.api_token import ApiToken
from app.utils.security import generate_token
from app.utils.crypto import hash_token

class TokenService:

    @staticmethod
    async def create(name, application):
        db = SessionLocal()

        try:
            plain_token = generate_token()

            token_hash = hash_token(
                plain_token
            )

            new_token = ApiToken(
                name=name,
                application=application,
                token=token_hash
            )

            db.add(new_token)
            db.commit()
            db.refresh(new_token)

            return {
                "id": new_token.id,
                "token": plain_token
            }

        finally:
            db.close()

    @staticmethod
    async def list(
        page=1,
        limit=20
    ):

        db = SessionLocal()

        try:

            query = db.query(ApiToken)


            total = query.count()


            tokens = (
                query
                .order_by(
                    ApiToken.created_at.desc()
                )
                .offset(
                    (page - 1) * limit
                )
                .limit(limit)
                .all()
            )


            return {
                "total": total,
                "page": page,
                "limit": limit,
                "data": tokens
            }


        finally:
            db.close()


    @staticmethod
    async def delete(token_id):

        db = SessionLocal()

        try:

            token = (
                db.query(ApiToken)
                .filter(ApiToken.id == token_id)
                .first()
            )

            if not token:
                return {
                    "message": "Token não encontrado"
                }

            db.delete(token)
            db.commit()

            return {
                "message": "Token removido"
            }

        finally:
            db.close()