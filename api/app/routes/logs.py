from fastapi import APIRouter, Query, Depends, HTTPException
from app.schemas.log import (LogSchema, LogListResponse, LogsBulkSchema)
from app.services.log_service import LogService
from app.dependencies.auth import get_current_user, verify_token

router = APIRouter()

@router.post("/logs")
async def create_log(
    log: LogSchema,
    token = Depends(verify_token)
):

    response = await LogService.create(
        log,
        token
    )

    return response

@router.post("/logs/bulk")
async def create_bulk_logs(
    payload: LogsBulkSchema,
    token = Depends(verify_token)
):

    return await LogService.create_bulk(
        payload.logs,
        token
    )

@router.get(
    "/logs",
    response_model=LogListResponse
)
async def get_logs(
    level: str | None = None,
    service: str | None = None,
    application: str | None = None,
    environment: str | None = None,
    search: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    page: int = 1,
    limit: int = 50,
    user = Depends(get_current_user)
):

    return await LogService.list(
        user=user,
        level=level,
        service=service,
        application=application,
        environment=environment,
        search=search,
        start_date=start_date,
        end_date=end_date,
        page=page,
        limit=limit
    )

@router.get("/logs/stats")
async def log_stats(
    user = Depends(get_current_user)
):

    return await LogService.stats(
        user=user
    )

@router.get("/logs/timeline")
async def log_timeline(
    minutes: int = Query(
        1440,
        ge=1,
        le=43200
    ),
    user = Depends(get_current_user)
):

    return await LogService.timeline(
        user=user,
        minutes=minutes
    )