from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime
import bcrypt
import psycopg2

app = FastAPI(title="auth-service")

# for input validation
class UserInput(BaseModel):
    username: str
    password: str

 # this will be for output validation
class UserOutput(BaseModel):
    id: int
    username: str
    created_at: datetime = Field(default_factory=datetime.now)

def hashed(password: str) -> bytes:
    byte_str = password.encode("utf-8")
    try:
        hashed_pass = bcrypt.hashpw(byte_str, bcrypt.gensalt())
    except TypeError as e:
        print(f"dev logs - {e}")
        raise
    except ValueError as e:
        print(f"dev logs - {e}")
        raise

    return hashed_pass

@app.post("/register")
async def register(username: str, password: str):
    conn = psycopg2.connect("dbname=test user=postgres password=secret port=5432")
    hash_pass = hashed(password)

    try:
        with conn.cursor() as cur: # opens cursor connection to perform db operations
            query = "INSERT INTO user_test (username, hashed_password) VALUES (%s, %s);"
            data_to_insert = (username, hash_pass)
            cur.execute(query, data_to_insert)

            conn.commit()
            print("row sucessfully inserted")

    except Exception as e:
        # this is to undo changes if not completely successful
        conn.rollback()
        print(f"User couldnt be created: {e}")
        raise

    finally:
        conn.close()