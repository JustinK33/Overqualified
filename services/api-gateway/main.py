from fastapi import FastAPI
import httpx, os

app = FastAPI(title="event-platform")

test_url = os.getenv("TEST_SERVICE") or "http://127.0.0.1:8000"

@app.get("/")
async def root():   
    return {"message": "it works"}

@app.get("/test-httpx")
async def test():
    try:
        r = httpx.get(test_url)
        return r.json()
    except httpx.HTTPError as e:
        print(f"HTTP Exception for {e.request.url} - {e}")