from fastapi import FastAPI

app = FastAPI(title="testing server")

@app.get("/")
async def test():
    return {"message": "test server reached"}