from fastapi import HTTPException

from app.models.user import User
from app.models.enums import UserRole

from app.utils.security import hash_password


class UserService:


    @staticmethod
    def create(
        db,
        current_user,
        data
    ):

        user = User(
            organization_id=current_user.organization_id,
            name=data.name,
            email=data.email,
            password_hash=hash_password(data.password),
            role=data.role
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user



    @staticmethod
    def list(
        db,
        current_user
    ):

        return (
            db.query(User)
            .filter(
                User.organization_id == current_user.organization_id
            )
            .all()
        )



    @staticmethod
    def get(
        db,
        current_user,
        user_id
    ):

        user = (
            db.query(User)
            .filter(
                User.id == user_id
            )
            .first()
        )


        if not user:
            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado"
            )


        if (
            current_user.role != UserRole.SUPER_ADMIN
            and user.organization_id != current_user.organization_id
        ):
            raise HTTPException(
                status_code=403,
                detail="Sem acesso ao usuário"
            )


        return user



    @staticmethod
    def update(
        db,
        current_user,
        user_id,
        data
    ):

        user = UserService.get(
            db,
            current_user,
            user_id
        )


        if data.name:
            user.name = data.name

        if data.email:
            user.email = data.email

        if data.role:
            user.role = data.role

        if data.active is not None:
            user.active = data.active


        db.commit()
        db.refresh(user)

        return user



    @staticmethod
    def delete(
        db,
        current_user,
        user_id
    ):

        user = UserService.get(
            db,
            current_user,
            user_id
        )


        db.delete(user)
        db.commit()


        return {
            "message": "Usuário removido"
        }