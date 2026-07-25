from fastapi import APIRouter, Query, Depends, HTTPException
from app.schemas.log import LogSchema, LogResponse, LogListResponse
from app.services.log_service import LogService
from app.schemas.log import LogsBulkSchema
from app.dependencies.auth import verify_token

router = APIRouter()

@router.post("/logs")
async def create_log(
    log: LogSchema,
    token = Depends(verify_token)
):

    if log.application != token.application:
        raise HTTPException(
            status_code=403,
            detail="Token não pertence a esta aplicação"
        )

    response = await LogService.create(log)

    return response


@router.get("/logs", response_model=LogListResponse)
async def get_logs(
    level: str | None = None,
    service: str | None = None,
    application: str | None = None,
    environment: str | None = None,
    search: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    page: int = 1,
    limit: int = 50
):

    return await LogService.list(
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
async def log_stats():

    return await LogService.stats()

@router.get("/logs/timeline")
async def log_timeline(
    minutes: int = Query(
        1440,
        ge=1,
        le=43200,
        description="Quantidade de minutos para análise"
    )
):

    return await LogService.timeline(
        minutes=minutes
    )

@router.post("/logs/bulk")
async def create_bulk_logs(
    payload: LogsBulkSchema,
    token=Depends(verify_token)
):

    for log in payload.logs:

        if log.application != token.application:
            raise HTTPException(
                status_code=403,
                detail=f"Token não pertence à aplicação '{log.application}'"
            )

    return await LogService.create_bulk(payload.logs)