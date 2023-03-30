# FastAPI + REST API example (Contacts)
# https://stackoverflow.com/questions/32311366/alembic-util-command-error-cant-find-identifier
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session
from sqlalchemy import text   # sqlalchemy бо потрібні моделі
import uvicorn

from src.database.db_connect import get_db
from src.database.models import Contact  #, Cat, Owner
from src.routes import contacts  # notes, tags
from src.schemes import ContactModel, ContactResponse, CatToNameModel


app = FastAPI()  # our application

# визначення маршруту для модуля contacts:
app.include_router(contacts.router, prefix='/api')
'''
Функція include_router використовується для включення маршрутизації, визначеної в кожному модулі, 
а параметр prefix використовується для зазначення загального префікса URL для всіх маршрутів цього модуля
'''
# app.include_router(tags.router, prefix='/api')
# app.include_router(notes.router, prefix='/api')


@app.get("/")
async def root() -> dict:  # є маршрутом за замовчуванням для застосунку
    return {" Welcome! ": " The personal virtual assistant is ready to go, I'm kidding ^_^ "}


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)) -> dict:  #  Спецкласс формує тип Session
    """Check if the container (DB server) is up."""
    try:
        # Make request (зрозуміло що не буде зловмисного коду, але через text сирий запит треба переганяти)
        result = db.execute(text("SELECT 1")).fetchone()  # SELECT 1 - запит до БД, що знею все Ок
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly!")
        
        return {"ALERT": "Welcome to FastAPI! System ready!"}
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database!")


# https://fastapi.tiangolo.com/deployment/manually/
# https://stackoverflow.com/questions/70300675/fastapi-uvicorn-run-always-create-3-instances-but-i-want-it-1-instance
if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)  # host='0.0.0.0'


# @app.get("/contacts", response_model=List[ContactResponse], tags=['contacts'])
# async def get_contacts(limit: int = Query(10, le=500), offset: int = 0, db: Session = Depends(get_db)):
#     contacts = db.query(Contact).limit(limit).offset(offset).all()
#     return contacts


# @app.get("/contacts/{contact_id}", response_model=ContactResponse, tags=['contact'])
# async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
#     contact = db.query(Contact).filter_by(id=contact_id).first()
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
#     return contact


# @app.post("/contacts", response_model=ContactResponse, tags=['contact'])
# async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
#     contact = Contact(**body.dict())
#     db.add(contact)
#     db.commit()
#     db.refresh(contact)
#     return contact


# @app.put("/contacts/{contact_id}", response_model=ContactResponse, tags=['contact'])
# async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
#     contact = db.query(Contact).filter_by(id=contact_id).first()
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
#     contact.name = body.name
#     contact.last_name = body.last_name
#     contact.email = body.email
#     contact.phone = body.phone
#     contact.description = body.description
#     db.commit()
#     return contact


# @app.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT, tags=['contact'])
# async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
#     contact = db.query(Contact).filter_by(id=contact_id).first()
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
#     db.delete(contact)
#     db.commit()
#     return contact


# @app.patch("/contacts/{contact_id}/to_name", response_model=ContactResponse, tags=['contact'])
# async def to_name_contact(body: CatToNameModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
#     contact = db.query(Contact).filter_by(id=contact_id).first()
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
#     contact.name = body.name
#     db.commit()
#     return contact


# uvicorn main:app --host localhost --port 8000 --reload
# http://127.0.0.1:8000/api/healthchecker
# http://127.0.0.1:8000
