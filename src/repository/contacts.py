# функції, визначені в модулі репозиторію, для взаємодії з базою даних.
# Усі методи роботи бази даних із тегами
# виконують безпосередні операції, додавання, зміни та видалення тегів всередині бази даних
# Всі ці функції використовують SQLAlchemy ORM для взаємодії з базою даних.
from typing import List, Optional

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
