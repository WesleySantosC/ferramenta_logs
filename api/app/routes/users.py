from fastapi import APIRouter, Depends
from app.database.connection import SessionLocal
from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_admin
from app.schemas.user import(UserCreate, UserUpdate, UserResponse)
from app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



@router.post("/")
def create_user(
    data: UserCreate,
    user = Depends(require_admin),
    db = Depends(get_db)
):

    return UserService.create(
        db,
        user,
        data
    )



@router.get(
    "/",
    response_model=list[UserResponse]
)
def list_users(
    user = Depends(get_current_user),
    db = Depends(get_db)
):

    return UserService.list(
        db,
        user
    )



@router.get("/{user_id}")
def get_user(
    user_id:int,
    user = Depends(get_current_user),
    db = Depends(get_db)
):

    return UserService.get(
        db,
        user,
        user_id
    )



@router.put("/{user_id}")
def update_user(
    user_id:int,
    data:UserUpdate,
    user = Depends(require_admin),
    db = Depends(get_db)
):

    return UserService.update(
        db,
        user,
        user_id,
        data
    )



@router.delete("/{user_id}")
def delete_user(
    user_id:int,
    user = Depends(require_admin),
    db = Depends(get_db)
):

    return UserService.delete(
        db,
        user,
        user_id
    )