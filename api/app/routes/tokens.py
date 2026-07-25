from fastapi import APIRouter
from app.services.token_service import TokenService

router = APIRouter()

@router.post("/tokens")
async def create_token(
    name: str,
    application: str
):

    return await TokenService.create(
        name,
        application
    )

@router.get("/tokens")
async def get_tokens(
    page:int = 1,
    limit:int = 20
):

    return await TokenService.list(
        page,
        limit
    )

@router.delete("/tokens/{token_id}")
async def delete_token(token_id: int):

    return await TokenService.delete(token_id)