# API Gateway

## What it does
API Gateway: this is where all client facing request hit and get transfered to the other microservices

## Tech Stack

- Python
- FastAPI
- Uvicorn
- httpx

## Install and Run

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd services/core-api
uvicorn main:app --reload
```