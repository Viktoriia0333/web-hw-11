from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models, schemas
from database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[schemas.ContactOut])
def upcoming_birthdays(db: Session = Depends(get_db)):
    today = datetime.today().date()
    upcoming = today + timedelta(days=7)
    contacts = db.query(models.Contact).all()
    result = []
    for c in contacts:
        birthday_this_year = c.birthday.replace(year=today.year)
        if today <= birthday_this_year <= upcoming:
            result.append(c)
    return result