from fastapi import FastAPI, HTTPException
import bcrypt, psycopg2, os
from models import UserInput, UserOutput
import jwt
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="auth-service")

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
async def register(user: UserInput):
    conn = psycopg2.connect(dbname=os.getenv("POSTGRES_DB"), user=os.getenv("POSTGRES_USER"), password=os.getenv("POSTGRES_PASSWORD"), host=os.getenv("DB_HOST") ,port=os.getenv("DB_PORT"))
    hash_pass = hashed(user.password)

    try:
        with conn.cursor() as cur: # opens cursor connection to perform db operations
            query = "INSERT INTO users (username, hashed_password) VALUES (%s, %s);"
            data_to_insert = (user.username, hash_pass)
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

@app.post("/login")
async def login(user: UserInput):
    key = os.getenv("SECRET_KEY")
    # stop at missing or empty key bc we dont want to break the sigining of the JTWs. and 500 makes sense since its a server error
    if not key:
        raise HTTPException(status_code=500, detail="Auth service misconfigured")
        
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"), 
        user=os.getenv("POSTGRES_USER"), 
        password=os.getenv("POSTGRES_PASSWORD"), 
        host=os.getenv("DB_HOST"), 
        port=os.getenv("DB_PORT")
    )
    
    try:
        with conn.cursor() as cur:
            query = "SELECT hashed_password FROM users WHERE username = (%s);"
            cur.execute(query, (user.username, ))
            hashed_pass = cur.fetchone() # i set this as the pass since cur.execute return None
            # this solves the raised None type warning in the check pw
            if not hashed_pass or hashed_pass is None:
                raise TypeError("The password is none or doesnt exists")
            elif bcrypt.checkpw(user.password.encode("utf-8"), hashed_pass[0]):
                encoded = jwt.encode({"user": user.username}, key, algorithm="HS256")
                return encoded
    except Exception as e:
        conn.rollback()
        print(f"Login failed: {e}")
        raise
    
    finally:
        conn.close()

# jwt func
# access token (usually 15 min - 1 hr) and refresh token (longer lived one)

# A new psycopg2.connect() on every request is expensive and doesn't scale. Look up connection pooling, psycopg2.pool 
# or an async driver like asyncpg since your route is async def already.

# print(f"Login failed: {e}") in production code: what's the standard library module 
# for this that gives you levels, timestamps, and configurable output?

# When auth fails, what should the client actually get back? Right now a failed check pw returns nothing and raises an unbound 
# var error, not a proper 401. What does FastAPI give you for returning specific status codes?

# Distinguishing "user not found" from "wrong password" in your error messages is a security smell. 
# Do you know why, and what the standard response is regardless of which one failed?