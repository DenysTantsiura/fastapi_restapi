# функції, визначені в модулі репозиторію, для взаємодії з базою даних.
# Усі методи роботи бази даних із тегами
# виконують безпосередні операції, додавання, зміни та видалення тегів всередині бази даних
# Всі ці функції використовують SQLAlchemy ORM для взаємодії з базою даних.
from datetime import date, timedelta
from typing import List, Optional
from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemes import ContactModel, ContactResponse, CatToNameModel


async def get_contacts(limit: int, offset: int, db: Session) -> List[Contact]:
    """Для отримання списку тегів з бази даних з можливістю пропустити певну кількість записів та обмежити 
    їх кількість, що повертаються. """
    return db.query(Contact).limit(limit).offset(offset).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    """Функція використовується для отримання певного запису за його ідентифікатором."""
    # return db.query(Contact).filter(Contact.id == contact_id).first()
    return db.query(Contact).filter_by(id=contact_id).first()  


async def create_contact(body: ContactModel, db: Session) -> Contact:
    """створення нового запису в базі даних. Бере об'єкт ContactModel і використовує інформацію з нього 
    для створення нового об'єкта Contact, потім додає його до сеансу і фіксує зміни в базі даних."""
    contact = db.query(Contact).filter_by(email=body.email, phone=body.phone).first() or \
                db.query(Contact).filter_by(name=body.name, last_name=body.last_name).first() 
    if contact:  # raise формує свою відповідь взамін return (все що після - відміняється):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Duplicate data')
    
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Optional[Contact]:
    """оновлення певного запису за його ідентифікатором. Бере об'єкт ContactModel та оновлює 
    за ім'ям запису інформацію з нього. Якщо запису не існує - повертається None."""
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


async def remove_contact(contact_id: int, db: Session)  -> Optional[Contact]:
    """видалення певного тега за його ідентифікатором. Якщо тега не існує, повертається None/"""
    # contact = db.query(Contact).filter(Contact.id == contact_id).first()
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def change_name_contact(body: CatToNameModel, contact_id: int, db: Session)  -> Optional[Contact]:
    """для оновлення лише імені кв записі."""
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        contact.name = body.name
        db.commit()
    return contact

async def search_by_name(name: str, db: Session) -> Contact:
    """Функція використовується для пошуку запису за певним іменем."""
    # return db.query(Contact).filter(Contact.name == name).first()  # .all()
    return db.query(Contact).filter_by(name=name).first()


async def search_by_last_name(last_name: str, db: Session) -> Contact:
    """Функція використовується для пошуку запису за певним прізвищем."""
    # return db.query(Contact).filter(Contact.last_name == last_name).first()
    return db.query(Contact).filter_by(last_name=last_name).first() 


async def search_by_email(email: str, db: Session) -> Contact:
    """Функція використовується для пошуку запису за певним email."""
    # return db.query(Contact).filter(Contact.email == email).first()
    return db.query(Contact).filter_by(email=email).first()


async def search_by_phone(phone: int, db: Session) -> Contact:
    """Функція використовується для пошуку запису за певним phone."""
    # return db.query(Contact).filter(Contact.phone == phone).first()
    return db.query(Contact).filter_by(phone=phone).first()


# https://stackoverflow.com/questions/4926757/sqlalchemy-query-where-a-column-contains-a-substring
async def search_by_like_name(part_name: str, limit: int, offset: int, db: Session) -> List[Contact]:
    """Функція використовується для пошуку запису за частковим співпадінням в імені."""
    return db.query(Contact).filter(Contact.name.icontains(part_name)).limit(limit).offset(offset).all()


async def search_by_like_last_name(part_last_name: str, limit: int, offset: int, db: Session) -> List[Contact]:
    """Функція використовується для пошуку запису за частковим співпадінням в прізвищем."""
    return db.query(Contact).filter(Contact.last_name.icontains(part_last_name)).limit(limit).offset(offset).all() 


async def search_by_like_email(part_email: str, limit: int, offset: int, db: Session) -> List[Contact]:
    """Функція використовується для пошуку запису за частковим співпадінням в email."""
    return db.query(Contact).filter(Contact.email.icontains(part_email)).limit(limit).offset(offset).all()


async def search_by_like_phone(part_phone: int, limit: int, offset: int, db: Session) -> List[Contact]:
    """Функція використовується для пошуку запису за частковим співпадінням в phone."""
    # return db.query(Contact).filter(Contact.phone == phone).first()
    return db.query(Contact).filter(Contact.phone.icontains(part_phone)).limit(limit).offset(offset).all()


def fortunate(days: int, birthday: date, today: date) -> bool:  # async/await ?
    """Return True or False if святкуватиме дні народження протягом наступних (days) днів."""
    happy_day: date = date(year=today.year, month=birthday.month, day=birthday.day)
    days_left: timedelta = happy_day - today
    if days_left.days <= 0:
        happy_day = date(year=today.year+1, month=birthday.month, day=birthday.day)

        return (happy_day - today).days <= days

    return days_left.days <= days
    # return date(year=birthday.year, month=today.month, day=today.day) - birthday <= timedelta(days)


async def search_by_birthday_celebration_within_days(meantime: int, limit: int, offset: int, db: Session) -> List[Contact]:
    """Функція використовується для пошуку контактів, що святкуватимуть дні народження протягом наступних (meantime) днів."""
    contacts = db.query(Contact).all()
    current_date = date.today()
    lucky_ones = [contact 
                  for contact in contacts 
                  if contact.birthday and fortunate(meantime, contact.birthday, current_date)]

    return lucky_ones[offset:offset+limit]
