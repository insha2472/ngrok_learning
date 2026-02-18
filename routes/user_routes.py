from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import User
from repositories.user_repo import UserRepo
from schemas.user_schemas import UserSchema

router = APIRouter()


# Create user
@router.post("/users")
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    user_repo = UserRepo(db)
    db_user = User(name=user.name, email=user.email, password=user.password)
    user_repo.add_user(db_user)
    return {"id": db_user.id, "name": db_user.name, "email": db_user.email}


# Get all users
@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    user_repo = UserRepo(db)
    users = user_repo.get_all_users()
    return [{"id": u.id, "name": u.name, "email": u.email} for u in users]


# Get user by ID
@router.get("/users/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user_repo = UserRepo(db)
    user = user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email}