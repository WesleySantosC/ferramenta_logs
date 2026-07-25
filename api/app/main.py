from fastapi import FastAPI
from app.database.connection import engine, Base
from app.models.log import Log
from app.routes.logs import router as logs_router
from app.models.api_token import ApiToken
from app.routes.tokens import router as tokens_router
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health

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
app.include_router(logs_router)
app.include_router(tokens_router)
app.include_router(health.router)
