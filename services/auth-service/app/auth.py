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
            query = "SELECT hashed_password FROM users WHERE username = %s;"
            cur.execute(
                query, 
                (user.username,)
            )
            row = cur.fetchone() # i set this as the pass since cur.execute return None
            # this solves the raised None type warning in the check pw
            if not row or not bcrypt.checkpw(
                user.password.encode("utf-8"), 
                bytes(row[0])
            ):
                raise HTTPException(status_code=401, detail="invalid username or password")

            token = jwt.encode({"user": user.username}, key, algorithm="HS256")
            # eventually we should include the payload info too like:
            # "exp": for expiration time, "sub": standard user identity claim, "type": access or refresh
            return {"access_token": token, "type_type": "bearer"}
    
    finally:
        conn.close()

# jwt func
# access token (usually 15 min - 1 hr) and refresh token (longer lived one)

# A new psycopg2.connect() on every request is expensive and doesn't scale. Look up connection pooling, psycopg2.pool 
# or an async driver like asyncpg since your route is async def already.

@app.post("/refresh")
async def refresh():
    pass # create a refresh token endpoint
    # refresh token -> new access token
    # initally have it set a 1 hr exp
    

# eventually we should implement prtected endpoints: require access token (or add a decorater)

@app.post("/logout")
async def logout():
    pass # create logout endpoint
    # should invalidate refresh token and excelidraw it b4 anything