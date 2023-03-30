# функції для взаємодії з базою даних.
from datetime import date, timedelta
from typing import List, Optional, Type

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemes import ContactModel, CatToNameModel


async def get_contacts(limit: int,
                       offset: int,
                       db: Session) -> Optional[List[Contact]]:
    """To retrieve a list of records from a database with the ability to skip 
    a certain number of records and limit the number returned."""
    return db.query(Contact).limit(limit).offset(offset).all()


async def get_contact(contact_id: int,
                      db: Session) -> Optional[Contact]:
    """To get a particular record by its ID."""
    # return db.query(Contact).filter(Contact.id == contact_id).first()
    return db.query(Contact).filter_by(id=contact_id).first()  


async def create_contact(body: ContactModel,
                         db: Session) -> Optional[Contact]:
    """Creating a new record in the database. Takes a ContactModel object and uses the information 
    from it to create a new Contact object, then adds it to the session and 
    commits the changes to the database."""
    contact = (db.query(Contact).filter_by(email=body.email).first() or
               db.query(Contact).filter_by(phone=body.phone).first() or
               db.query(Contact).filter_by(name=body.name, last_name=body.last_name).first())
    if contact:  # raise формує свою відповідь взамін return (все що після - відміняється):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Duplicate data')
    
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int,
                         body: ContactModel,
                         db: Session) -> Optional[Contact]:
    """Update a specific record by its ID. Takes the ContactModel object and updates the information from it 
    by the name of the record. If the record does not exist - None is returned."""
    # contact = db.query(Contact).filter(contact.id == contact_id).first()
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        contact.name = body.name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.description = body.description
        db.commit()
    return contact


async def remove_contact(contact_id: int,
                         db: Session) -> Optional[Contact]:
    """Delete a specific record by its ID. If the record does not exist - None is returned."""
    # contact = db.query(Contact).filter(Contact.id == contact_id).first()
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def change_name_contact(body: CatToNameModel,
                              contact_id: int,
                              db: Session) -> Optional[Contact]:
    """To update only the name of the record."""
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        contact.name = body.name
        db.commit()
    return contact


async def search_by_name(name: str,
                         db: Session) -> Optional[Contact]:
    """To search for a record by a specific name."""
    # return db.query(Contact).filter(Contact.name == name).first()  # .all()
    return db.query(Contact).filter_by(name=name).first()


async def search_by_last_name(last_name: str,
                              db: Session) -> Optional[Contact]:
    """To search for a record by a specific last name."""
    # return db.query(Contact).filter(Contact.last_name == last_name).first()
    return db.query(Contact).filter_by(last_name=last_name).first() 


async def search_by_email(email: str,
                          db: Session) -> Optional[Contact]:
    """To search for a record by a certain email."""
    # return db.query(Contact).filter(Contact.email == email).first()
    return db.query(Contact).filter_by(email=email).first()


async def search_by_phone(phone: int,
                          db: Session) -> Optional[Contact]:
    """To search for a record by a certain phone."""
    # return db.query(Contact).filter(Contact.phone == phone).first()
    return db.query(Contact).filter_by(phone=phone).first()


# https://stackoverflow.com/questions/4926757/sqlalchemy-query-where-a-column-contains-a-substring
async def search_by_like_name(part_name: str,
                              limit: int,
                              offset: int,
                              db: Session) -> Optional[List[Contact]]:
    """To search for an entry by a partial match in the name."""
    return db.query(Contact).filter(Contact.name.icontains(part_name)).limit(limit).offset(offset).all()


async def search_by_like_last_name(part_last_name: str,
                                   limit: int,
                                   offset: int,
                                   db: Session) -> Optional[List[Contact]]:
    """To search for a record by a partial match in the last name."""
    return db.query(Contact).filter(Contact.last_name.icontains(part_last_name)).limit(limit).offset(offset).all() 


async def search_by_like_email(part_email: str,
                               limit: int,
                               offset: int,
                               db: Session) -> Optional[List[Contact]]:
    """To search for a record by a partial match in an email."""
    return db.query(Contact).filter(Contact.email.icontains(part_email)).limit(limit).offset(offset).all()


async def search_by_like_phone(part_phone: int,
                               limit: int,
                               offset: int,
                               db: Session) -> Optional[List[Contact]]:
    """To search for a record by a partial match in phone."""
    # return db.query(Contact).filter(Contact.phone == phone).first()
    return db.query(Contact).filter(Contact.phone.icontains(part_phone)).limit(limit).offset(offset).all()


def fortunate(days: int,
              birthday: date,
              today: date) -> bool:  # async/await ?
    """Return the statement (true/false) will celebrate birthdays in the next (days) days?"""
    happy_day: date = date(year=today.year, month=birthday.month, day=birthday.day)
    days_left: timedelta = happy_day - today
    if days_left.days <= 0:
        happy_day = date(year=today.year+1, month=birthday.month, day=birthday.day)

        return (happy_day - today).days <= days

    return days_left.days <= days


async def search_by_birthday_celebration_within_days(meantime: int,
                                                     limit: int,
                                                     offset: int,
                                                     db: Session) -> Optional[List[Type[Contact]]]:
    """To find contacts celebrating birthdays in the next (meantime) days."""
    contacts = db.query(Contact).all()
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found") 
    current_date = date.today()
    lucky_ones = [contact 
                  for contact in contacts 
                  if contact.birthday and fortunate(meantime, contact.birthday, current_date)]

    return lucky_ones[offset:offset+limit]
