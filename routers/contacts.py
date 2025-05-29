from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas
from database import SessionLocal
from dependencies import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.ContactOut, status_code=201)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    db_contact = models.Contact(**contact.dict(), owner_id=user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@router.get("/", response_model=list[schemas.ContactOut])
def get_contacts(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return db.query(models.Contact).filter(models.Contact.owner_id == user.id).all()


@router.get("/{contact_id}", response_model=schemas.ContactOut)
def get_contact(contact_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    contact = db.query(models.Contact).filter_by(id=contact_id, owner_id=user.id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=schemas.ContactOut)
def update_contact(contact_id: int, updated: schemas.ContactUpdate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    contact = db.query(models.Contact).filter_by(id=contact_id, owner_id=user.id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for field, value in updated.dict().items():
        setattr(contact, field, value)
    db.commit()
    db.refresh(contact)
    return contact


@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    contact = db.query(models.Contact).filter_by(id=contact_id, owner_id=user.id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return {"message": "Contact deleted"}