from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse
from app.utils.jwt import create_access_token
from app.utils.security import verify_password
from app.models.organization import Organization
from app.utils.security import hash_password
from app.models.enums import UserRole

class AuthService:

    @staticmethod
    def login(
        db: Session,
        data: LoginRequest
    ) -> LoginResponse:

        # Procura usuário pelo e-mail
        user = (
            db.query(User)
            .filter(User.email == data.email)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha inválidos."
            )

        # Verifica se o usuário está ativo
        if not user.active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário desativado."
            )

        # Verifica a senha
        if not verify_password(
            data.password,
            user.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha inválidos."
            )

        # Gera o Access Token
        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "organization_id": user.organization_id,
                "role": user.role.value
            }
        )

        return LoginResponse(
            access_token=access_token,
            token_type="bearer"
        )
    
    @staticmethod
    def register(
        db,
        data
    ):


        organization = Organization(

            name=data.organization_name,

            slug=data.organization_name.lower()
            .replace(" ","-")

        )


        db.add(organization)

        db.flush()



        user = User(

            organization_id=organization.id,

            name=data.name,

            email=data.email,

            password_hash=hash_password(
                data.password
            ),

            role=UserRole.SUPER_ADMIN,

            active=True,

            must_change_password=False

        )


        db.add(user)

        db.commit()

        db.refresh(user)



        return {

            "message":
                "Cadastro realizado com sucesso",

            "organization_id":
                organization.id,

            "user_id":
                user.id

        }