# Роутер(маршрут) для модуля contacts - містить точки доступу для операцій CRUD
"""
код визначає набір маршрутів для модуля contacts з використанням класу APIRouter з бібліотеки fastapi. 
Маршрути прив'язані до певних операцій HTTP (GET, POST, PUT, DELETE) та призначені для обробки операцій 
CRUD контактів (contacts).

Маршрут router.get("/", response_model=List[ContactResponse]) прив'язаний до операції GET і призначений для отримання
списку контактів (contacts). Він приймає два необов'язкові параметри запиту, skip та limit, 
які використовуються для розбиття результатів на сторінки або іншими словами для пагінації.
"""
from typing import List, Optional

from fastapi import APIRouter, FastAPI, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session

from src.database.db_connect import get_db
from src.database.models import Contact
# from src.shemas import TagModel, TagResponse
# from src.repository import tags as repository_tags
from src.repository import contacts as repository_contacts
from src.schemes import ContactModel, ContactResponse, CatToNameModel


router = APIRouter(prefix='/contacts', tags=["contacts"])
# router = APIRouter(prefix='/tags', tags=["tags"])


@router.get("/", response_model=List[ContactResponse], tags=['all_contacts'])  # tags тільки для документації свагер 
async def get_contacts(limit: int = Query(10, le=500), offset: int = 0, db: Session = Depends(get_db)) -> Optional[List[Contact]]:
    contacts = await repository_contacts.get_contacts(limit, offset, db)

    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, tags=['contact'])  # name = 'Повернути контакт' - для документації
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)) -> Optional[Contact]:
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    
    return contact


@router.post("/", response_model=ContactResponse, tags=['contact'])
async def create_contact(body: ContactModel, db: Session = Depends(get_db)) -> Optional[Contact]:

    return await repository_contacts.create_contact(body, db)


@router.put("/{contact_id}", response_model=ContactResponse, tags=['contact'])
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)) -> Optional[Contact]:  # = Path(ge=1) ?
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")

    return contact


# response_model=ContactResponse or status_code=status.HTTP_204_NO_CONTENT ?
@router.delete("/{contact_id}", response_model=ContactResponse, tags=['contact'])
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    
    return contact


@router.patch("/{contact_id}/to_name", response_model=ContactResponse, tags=['contact'])
async def change_name_contact(body: CatToNameModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.change_name_contact(body, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    return contact


@router.get("/search_by_name/{name}", response_model=ContactResponse, tags=['search'])
async def search_by_name(name: str, db: Session = Depends(get_db)):
    contact = await repository_contacts.search_by_name(name, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    
    return contact


@router.get("/search_by_last_name/{last_name}", response_model=ContactResponse, tags=['search'])
async def search_by_last_name(last_name: str, db: Session = Depends(get_db)):
    contact = await repository_contacts.search_by_last_name(last_name, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    
    return contact


@router.get("/search_by_email/{email}", response_model=ContactResponse, tags=['search'])
async def search_by_email(email: str, db: Session = Depends(get_db)):
    contact = await repository_contacts.search_by_email(email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    
    return contact


@router.get("/search_by_phone/{phone}", response_model=ContactResponse, tags=['search'])
async def search_by_phone(phone: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.search_by_phone(phone, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    
    return contact


@router.get("/search_by_birthday_celebration_within_days/{days}", response_model=List[ContactResponse], tags=['search'])
async def search_by_birthday_celebration_within_days(days: int, limit: int = Query(10, le=500), offset: int = 0, db: Session = Depends(get_db)) -> Optional[List[Contact]]:
    contact = await repository_contacts.search_by_birthday_celebration_within_days(days, limit, offset, db)
    if contact is None:  # NoConnection in database...
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    
    return contact


@router.get("/search_by_like_name/{name}", response_model=List[ContactResponse], tags=['search'])
async def search_by_like_name(name: str, limit: int = Query(10, le=500), offset: int = 0, db: Session = Depends(get_db)) -> Optional[List[Contact]]:
    contact = await repository_contacts.search_by_like_name(name, limit, offset, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    
    return contact


@router.get("/search_by_like_last_name/{last_name}", response_model=List[ContactResponse], tags=['search'])
async def search_by_like_last_name(last_name: str, limit: int = Query(10, le=500), offset: int = 0, db: Session = Depends(get_db)) -> Optional[List[Contact]]:
    contact = await repository_contacts.search_by_like_last_name(last_name, limit, offset, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    
    return contact


@router.get("/search_by_like_email/{email}", response_model=List[ContactResponse], tags=['search'])
async def search_by_like_email(email: str, limit: int = Query(10, le=500), offset: int = 0, db: Session = Depends(get_db)) -> Optional[List[Contact]]:
    contact = await repository_contacts.search_by_like_email(email, limit, offset, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    
    return contact


@router.get("/search_by_like_phone/{phone}", response_model=List[ContactResponse], tags=['search'])
async def search_by_like_phone(phone: int, limit: int = Query(10, le=500), offset: int = 0, db: Session = Depends(get_db)) -> Optional[List[Contact]]:
    contact = await repository_contacts.search_by_like_phone(phone, limit, offset, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    
    return contact
