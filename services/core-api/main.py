from fastapi import FastAPI

app = FastAPI(title="event-platform")

@app.get("/")
async def root():
    return {"message": "it works"}