from pydantic import BaseModel, Field
from datetime import datetime

# for input validation
class UserInput(BaseModel):
    username: str
    password: str

# this will be for output validation
class UserOutput(BaseModel):
    id: int
    username: str
    created_at: datetime = Field(default_factory=datetime.now)