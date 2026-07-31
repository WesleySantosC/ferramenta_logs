from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.models.project import Project
from app.models.user import User
from app.models.project_member import ProjectMember
from app.models.enums import UserRole

from app.utils.security import hash_password


class BootstrapService:

    @staticmethod
    def initialize(db: Session):

        existing_user = (
            db.query(User)
            .first()
        )

        if existing_user:
            return


        print("Criando instalação inicial...")


        organization = Organization(
            name="Default Organization",
            slug="default"
        )

        db.add(organization)
        db.flush()


        project = Project(
            organization_id=organization.id,
            name="Default Project",
            description="Projeto inicial da plataforma"
        )

        db.add(project)
        db.flush()


        admin = User(
            organization_id=organization.id,
            name="Administrator",
            email="admin@email.com",
            password_hash=hash_password("123456"),
            role=UserRole.SUPER_ADMIN,
            active=True,
            must_change_password=True
        )

        db.add(admin)
        db.flush()


        project_member = ProjectMember(
            project_id=project.id,
            user_id=admin.id,
            role="ADMIN"
        )

        db.add(project_member)
        db.commit()

        print("==============================")
        print("Usuário administrador criado")
        print("Email: admin@email.com")
        print("Senha: 123456")
        print("==============================")