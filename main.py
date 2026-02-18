from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app = FastAPI()

# Create tables on startup (only if DB packages are installed)
@app.on_event("startup")
def on_startup():
    try:
        from db import engine, Base
        import models
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"⚠️ Could not create DB tables (will use in-memory): {e}")

# Hello World route
@app.get("/")
def read_root():
    return {"message": "Hello World"}


# Fake database
users_db = []

# Models
class User(BaseModel):
    name: str
    email: str

class UserResponse(User):
    user_id: str


# Create user
@app.post("/users", response_model=UserResponse)
def create_user(user: User):
    new_user = {
        "user_id": str(uuid4()),
        "name": user.name,
        "email": user.email
    }
    users_db.append(new_user)
    return new_user


# Get all users
@app.get("/users", response_model=List[UserResponse])
def get_all_users():
    return users_db


# Get user by ID
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: str):
    for user in users_db:
        if user["user_id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")