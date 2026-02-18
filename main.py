from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import json
import os

# In-memory database
students_db: dict[int, dict] = {}
users_db: List[dict] = []  # Mock user database
USERS_FILE = "users.json"

# Load users from file if exists
if os.path.exists(USERS_FILE):
    try:
        with open(USERS_FILE, "r") as f:
            users_db = json.load(f)
    except Exception as e:
        print(f"Error loading users: {e}")

def save_users():
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(users_db, f)
    except Exception as e:
        print(f"Error saving users: {e}")

current_id = 1


class Student(BaseModel):
    name: str
    email: str
    age: int
    Roll_no: str
    Department: str


class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    Roll_no: str
    Department: str


class UserSignup(BaseModel):
    email: str
    password: str
    name: str  # Added name


class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    user_name: str # Added user_name to response


class AskRequest(BaseModel):
    message: str
    system_prompt: str = "You are a helpful assistant."


class AskResponse(BaseModel):
    response: str


class ChatMessage(BaseModel):
    role: str
    content: str
    created_at: Optional[str] = None
    files: Optional[List[dict]] = []

class ChatSession(BaseModel):
    id: str
    title: str
    created_at: str
    messages: List[ChatMessage] = []

class ChatCreate(BaseModel):
    title: str

CHATS_FILE = "chats.json"
chats_db: List[dict] = []

if os.path.exists(CHATS_FILE):
    try:
        with open(CHATS_FILE, "r") as f:
            chats_db = json.load(f)
    except Exception as e:
        print(f"Error loading chats: {e}")

def save_chats():
    try:
        with open(CHATS_FILE, "w") as f:
            json.dump(chats_db, f)
    except Exception as e:
        print(f"Error saving chats: {e}")

@app.get("/chat/history", response_model=List[dict])
def get_history():
    # In a real app, we'd filter by user from the token
    return chats_db

@app.post("/chat/history")
def create_chat(chat_data: ChatCreate):
    import uuid
    from datetime import datetime
    new_chat = {
        "id": str(uuid.uuid4()),
        "title": chat_data.title,
        "created_at": datetime.now().isoformat(),
        "messages": []
    }
    chats_db.insert(0, new_chat) # Newest first
    save_chats()
    return new_chat

@app.post("/chat/history/{chat_id}/messages")
def add_message(chat_id: str, message: ChatMessage):
    chat = next((c for c in chats_db if c["id"] == chat_id), None)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    from datetime import datetime
    message_dict = message.model_dump()
    message_dict["created_at"] = datetime.now().isoformat()
    chat["messages"].append(message_dict)
    save_chats()
    return {"status": "success"}

@app.delete("/chat/history/{chat_id}")
def delete_chat(chat_id: str):
    global chats_db
    chats_db = [c for c in chats_db if c["id"] != chat_id]
    save_chats()
    return {"status": "deleted"}

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/signup")
def signup(user: UserSignup):
    # Check if user exists (mock check)
    for existing_user in users_db:
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")

    users_db.append(user.model_dump())
    save_users()
    return {"message": "User created successfully", "email": user.email, "name": user.name}


@app.post("/login", response_model=Token)
def login(creds: LoginRequest):
    # Mock authentication
    user = next((u for u in users_db if u["email"] == creds.email), None)
    if not user:
         # Mock behavior: allows login if user not found (for testing persistence across restarts)
         # Try to derive a name from the email for a better experience
         mock_name = creds.email.split("@")[0].replace(".", " ").title()
         user = {"email": creds.email, "name": mock_name, "password": creds.password}
    
    # Verify password (mock)
    if user.get("password") != creds.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {
        "access_token": "mock_access_token_jwt_string",
        "token_type": "bearer",
        "refresh_token": "mock_refresh_token_string",
        "user_name": user.get("name", "Ziggy Friend")
    }


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    # Mock AI logic
    # Instant response as requested
    user_message = request.message.lower()
    system_prompt = request.system_prompt.upper()
    
    if "ziggy" in user_message:
        return {"response": "Hello! I'm **Ziggy**, your friendly AI companion. 🐱 How can I assist you today? I can help with research, study, or even generate images!"}
    
    if "IMAGE GENERATION" in system_prompt:
        return {"response": "I've created this image for you based on your description! 🎨\n\nIMAGE_URL: https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba"}
    
    if "search" in user_message:
        return {"response": "### Search Results for your query:\n\n1. **Ziggy AI**: A fast and cute assistant.\n2. **FastAPI**: The powerful engine behind this chat.\n3. **React**: Providing the smooth, interactive UI you're using right now.\n\nIs there anything specific from these you'd like to dive into?"}

    return {"response": f"That's an interesting point about '{request.message}'. \n\nDirectly speaking, as a **demo bot**, I don't have a real brain yet, but I can certainly help you explore the features of this **premium dashboard**! \n\n- Try attaching a file 📎\n- Toggle **Study Mode** 📚\n- Ask me to **generate an image** 🎨"}


@app.post("/students", response_model=StudentResponse)
def create_student(student: Student):
    global current_id
    student_data = student.model_dump()
    student_data["id"] = current_id
    students_db[current_id] = student_data
    current_id += 1
    return student_data


@app.get("/students/{id}", response_model=StudentResponse)
def get_student(id: int):
    if id not in students_db:
        return {"error": "Student not found"}
    return students_db[id]


@app.get("/students", response_model=List[StudentResponse])
def get_all_students():
    return list(students_db.values())


@app.put("/students/{id}", response_model=StudentResponse)
def update_student(id: int, student: Student):
    if id not in students_db:
        return {"error": "Student not found"}
    student_data = student.model_dump()
    student_data["id"] = id
    students_db[id] = student_data
    return student_data


@app.delete("/students/{id}")
def delete_student(id: int):
    if id not in students_db:
        return {"error": "Student not found"}
    deleted_student = students_db.pop(id)
    return {"message": "Student deleted", "student": deleted_student}