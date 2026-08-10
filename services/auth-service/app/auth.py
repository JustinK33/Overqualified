from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime
import bcrypt

app = FastAPI(title="auth-service")

user_id_count = 0 # find a way to auto increment it later

class User(BaseModel):
    id: int
    username: str
    password: str #hashvalue
    created_at: datetime = Field(default_factory=datetime.now)

def hashed(password: bytes):
    hashed_pass = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_pass

@app.get("/register")
async def register(username: str, password: str):
    pass