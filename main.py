from fastapi import FastAPI
from db import engine, Base
import models
from routes.user_routes import router

app = FastAPI()

# Create tables on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created!")

# Hello World route
@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Include all user routes (signup, login, /users, /users/{id}, refresh)
app.include_router(router)