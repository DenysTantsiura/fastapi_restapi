# Роутер(маршрут) для модуля contacts - містять точки доступу для операцій CRUD
"""
код визначає набір маршрутів для модуля contacts з використанням класу APIRouter з бібліотеки fastapi. 
Маршрути прив'язані до певних операцій HTTP (GET, POST, PUT, DELETE) та призначені для обробки операцій 
CRUD контактів (contacts).

Маршрут router.get("/", response_model=List[ContactResponse]) прив'язаний до операції GET і призначений для отримання 
списку контактів (contacts). Він приймає два необов'язкові параметри запиту, skip та limit, які використовуються для розбиття 
результатів на сторінки або іншими словами для пагінації.
"""
from typing import List

from fastapi import APIRouter, FastAPI, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session

from src.database.db_connect import get_db
from src.database.models import Contact
from src.schemes import ContactModel, ContactResponse, CatToNameModel
# from src.shemas import TagModel, TagResponse
# from src.repository import tags as repository_tags
from src.repository import contacts as repository_contacts


router = APIRouter(prefix='/contacts', tags=["contacts"])
# router = APIRouter(prefix='/tags', tags=["tags"])


@router.get("/", response_model=List[ContactResponse], tags=['contacts'])
async def get_contacts(limit: int = Query(10, le=500), offset: int = 0, db: Session = Depends(get_db)):
    # contacts = db.query(Contact).limit(limit).offset(offset).all()
    contacts = await repository_contacts.get_contacts(limit, offset, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, tags=['contact'])
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    # contact = db.query(Contact).filter_by(id=contact_id).first()
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    return contact


@router.post("/", response_model=ContactResponse, tags=['contact'])
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    # contact = Contact(**body.dict())
    # db.add(contact)
    # db.commit()
    # db.refresh(contact)
    # return contact
    return await repository_contacts.create_contact(body, db)


@router.put("/{contact_id}", response_model=ContactResponse, tags=['contact'])
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):  # = Path(ge=1) ?
    # contact = db.query(Contact).filter_by(id=contact_id).first()
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    # contact.name = body.name
    # contact.last_name = body.last_name
    # contact.email = body.email
    # contact.phone = body.phone
    # contact.description = body.description
    # db.commit()
    return contact


# response_model=ContactResponse or status_code=status.HTTP_204_NO_CONTENT ?
@router.delete("/{contact_id}", response_model=ContactResponse, tags=['contact'])
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    # contact = db.query(Contact).filter_by(id=contact_id).first()
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    # db.delete(contact)
    # db.commit()
    return contact


@router.patch("/{contact_id}/to_name", response_model=ContactResponse, tags=['contact'])
async def to_name_contact(body: CatToNameModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    # contact = db.query(Contact).filter_by(id=contact_id).first()
    contact = await repository_contacts.change_name_contact(body, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    # contact.name = body.name
    # db.commit()
    return contact

'''Контакти повинні бути доступні для 
пошуку за 

іменем, 
прізвищем чи 
адресою електронної пошти (Query).

API повинен мати змогу отримати 
список контактів з днями народження на 
найближчі 
7 днів.'''
