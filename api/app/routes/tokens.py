from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.services.token_service import TokenService
from app.schemas.token import TokenCreateSchema
from app.dependencies.auth import get_current_user, get_db

from app.dependencies.project_access import verify_project_access


router = APIRouter()


@router.post("/tokens")
async def create_token(
    payload: TokenCreateSchema,
    user = Depends(get_current_user)
):

    return await TokenService.create(
        payload,
        user
    )

@router.get("/tokens")
async def get_tokens(
    user = Depends(get_current_user),
    db: Session = Depends(get_db),
    page:int = 1,
    limit:int = 20
):

    return await TokenService.list(
        organization_id=user.organization_id,
        page=page,
        limit=limit
    )



@router.delete("/tokens/{token_id}")
async def delete_token(
    token_id:int,
    user = Depends(get_current_user)
):

    return await TokenService.delete(
        token_id
    )