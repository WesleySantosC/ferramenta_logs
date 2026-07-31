from app.database.connection import SessionLocal
from app.models.api_token import ApiToken
from app.models.project import Project
from app.utils.security import generate_token
from app.utils.crypto import hash_token
from app.dependencies.project_access import verify_project_access


class TokenService:


    @staticmethod
    async def create(
        payload,
        user
    ):

        db = SessionLocal()

        try:

            project = verify_project_access(
                db,
                user,
                payload.project_id
            )


            plain_token = generate_token()

            token_hash = hash_token(
                plain_token
            )


            new_token = ApiToken(
                name=payload.name,
                project_id=project.id,
                application=project.name,
                token=token_hash
            )


            db.add(new_token)
            db.commit()
            db.refresh(new_token)


            return {
                "id": new_token.id,
                "token": plain_token,
                "application": project.name,
                "project_id": project.id
            }


        finally:
            db.close()

    @staticmethod
    async def list(
        organization_id,
        page=1,
        limit=20
    ):

        db = SessionLocal()


        try:

            from app.models.project import Project


            tokens = (
                db.query(ApiToken)
                .join(Project)
                .filter(
                    Project.organization_id == organization_id
                )
                .offset(
                    (page-1)*limit
                )
                .limit(limit)
                .all()
            )


            return {

                "data": tokens,

                "page": page,

                "limit": limit

            }


        finally:

            db.close()



    @staticmethod
    async def delete(
        token_id
    ):

        db = SessionLocal()


        try:

            token = (
                db.query(ApiToken)
                .filter(
                    ApiToken.id == token_id
                )
                .first()
            )


            if not token:

                return {
                    "message":"Token não encontrado"
                }


            db.delete(token)

            db.commit()


            return {
                "message":"Token removido"
            }


        finally:

            db.close()