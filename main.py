import os

import uvicorn
from fastapi import FastAPI

from routes import contacts, auth, birthdays
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import aioredis

load_dotenv()


app = FastAPI(title="Contacts API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(contacts.router, prefix="/api/contacts", tags=["Contacts"])
app.include_router(birthdays.router, prefix="/api/birthdays", tags=["Birthdays"])


@app.on_event("startup")
async def startup():
    redis = await aioredis.from_url(os.getenv("REDIS_URL"), encoding="utf8", decode_responses=True)
    await FastAPILimiter.init(redis)


@app.get("/")
def read_root():
    return {"message": "This is Contacts API"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)