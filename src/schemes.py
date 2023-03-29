# схеми для валідації наших вхідних та вихідних даних
# Створимо моделі Pydantic, що визначають дійсну форму даних
# Загалом, ці моделі визначають поля та правила валідації для створення, оновлення та отримання даних для...
from datetime import date
from pydantic import BaseModel, Field, EmailStr  # poetry add pydantic[email] # https://github.com/JoshData/python-email-validator


# https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
# https://github.com/tiangolo/fastapi/issues/5201#issuecomment-1197609410
class ContactModel(BaseModel):
    name: str = Field(default='Unknown', min_length=2, max_length=30)
    last_name: str = Field(default='Unknown', min_length=2, max_length=40)
    email: EmailStr  # str =  Field(default='Unknown@mail.com', min_length=6, max_length=30, regex=...)  # i@i.ua
    phone: int = Field(default=1, gt=0, le=9999999999999999)  # not started from 0 !!!
    birthday: date  # = Field(default=date.today())  # YYYY-MM-DD
    description: str = Field(default='-', max_length=3000)  # String


class ContactResponse(ContactModel):
    id: int = 1  # якщо 0 дратує

    class Config:  # дружимо клас з відповідною моделлю з моделей ?
        orm_mode = True  # дані повертаються з БД
'''
Атрибут orm_mode у класі Config використовується для увімкнення режиму ORM для цієї моделі. 
Таким чином, атрибут orm_mode у класі Config дозволяє Pydantic автоматично генерувати модель 
бази даних з певних полів, що дозволяє використовувати модель Pydantic як об'єкт передачі даних, 
а також як модель бази даних без необхідності окремого використання моделі бази даних. 
'''

class CatToNameModel(BaseModel):
    name: str = Field(default='Unknown-next', min_length=2, max_length=30)


# class OwnerModel(BaseModel):
#     email: EmailStr


# class OwnerResponse(BaseModel):
#     id: int = 1
#     email: EmailStr

#     class Config:
#         orm_mode = True


# class CatModel(BaseModel):
#     nickname: str = Field('Mur4ik', min_length=3, max_length=16)
#     age: int = Field(1, ge=0, le=30)
#     vaccinated: bool = False
#     description: str
#     owner_id: int = Field(1, gt=0)


# class CatVaccinatedModel(BaseModel):
#     vaccinated: bool = False


# class CatResponse(BaseModel):
#     id: int = 1
#     nickname: str
#     age: int
#     vaccinated: bool
#     description: str
#     owner: OwnerResponse

#     class Config:
#         orm_mode = True
