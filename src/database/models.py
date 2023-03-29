from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database.db_connect import Base, engine

'''
з використанням декларативної системи SQLAlchemy. Клас Base - це декларативний базовий клас, 
що надається SQLAlchemy, який використовується для визначення структури класів 
та наслідування від нього.'''
class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), index=True)
    last_name = Column(String(40), index=True)
    email = Column(String(30), unique=True, index=True)
    phone = Column(Integer, unique=True, index=True)  # !!! type int no take arguments Integer(16) 
    birthday = Column(Date, index=True)
    description = Column(String(3000))

'''
Виконуємо міграції моделей
Створивши файл з моделями, потрібно виконати процес міграції за допомогою alembic. 
Насамперед необхідно ініціалізувати оточення alembic за допомогою команди:
alembic init migrations
'''

# class Owner(Base):
#     __tablename__ = "owners"
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)


# class Cat(Base):
#     __tablename__ = "cats"
#     id = Column(Integer, primary_key=True, index=True)
#     nickname = Column(String, index=True)
#     age = Column(Integer)
#     vaccinated = Column(Boolean, default=False)
#     description = Column(String)
#     owner_id = Column(Integer, ForeignKey("owners.id"), nullable=True)
#     owner = relationship("Owner", backref="cats")


# Base.metadata.create_all(bind=engine)
