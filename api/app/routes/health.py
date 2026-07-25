from fastapi import APIRouter
from sqlalchemy import text

from app.database.connection import SessionLocal
from app.database.redis import redis_client


router = APIRouter()


@router.get("/health")
async def health():

    status = {
        "status": "healthy",
        "database": "unknown",
        "redis": "unknown"
    }


    try:
        db = SessionLocal()

        db.execute(
            text("SELECT 1")
        )

        status["database"] = "ok"

        db.close()


    except Exception:

        status["database"] = "error"
        status["status"] = "unhealthy"



    try:

        redis_client.ping()

        status["redis"] = "ok"


    except Exception:

        status["redis"] = "error"
        status["status"] = "unhealthy"



    return status