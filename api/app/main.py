from fastapi import FastAPI
from app.database.connection import engine, Base, SessionLocal
from app.models.log import Log
from app.routes.logs import router as logs_router
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health

from app.models.organization import Organization
from app.models.user import User
from app.models.project import Project
from app.models.api_token import ApiToken

from app.routes.auth import router as auth_router
from app.routes.tokens import router as tokens_router
from app.services.bootstrap_service import BootstrapService
from app.routes.organizations import router as organizations_router
from app.routes.projects import router as projects_router
from app.routes.users import router as users_router


app = FastAPI(
    title="OpenObserve API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    BootstrapService.initialize(db)
finally:
    db.close()

app.include_router(health.router)
app.include_router(auth_router)
app.include_router(logs_router)
app.include_router(tokens_router)
app.include_router(organizations_router)
app.include_router(projects_router)
app.include_router(users_router)