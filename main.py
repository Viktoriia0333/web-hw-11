import uvicorn
from fastapi import FastAPI

from routers import contacts
from routers import birthdays

app = FastAPI(title="Contacts API")

app.include_router(contacts.router, prefix="/api/contacts", tags=["Contacts"])
app.include_router(birthdays.router, prefix="/api/birthdays", tags=["Birthdays"])


@app.get("/")
def read_root():
    return {"message": "This is Contacts API"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)