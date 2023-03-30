# Схеми для валідації вхідних та вихідних даних
from datetime import date
from pydantic import BaseModel, Field, EmailStr  # poetry add pydantic[email] 


class ContactModel(BaseModel):
    name: str = Field(default='Unknown', min_length=2, max_length=30)
    last_name: str = Field(default='Unknown', min_length=2, max_length=40)
    email: EmailStr  # str =  Field(default='Unknown@mail.com', min_length=6, max_length=30, regex=...)  # i@i.ua
    phone: int = Field(default=1, gt=0, le=9999999999999999)
    birthday: date  # = Field(default=date.today())  # YYYY-MM-DD
    description: str = Field(default='-', max_length=3000)  # String


class ContactResponse(ContactModel):
    id: int = 1 

    class Config:
        orm_mode = True


class CatToNameModel(BaseModel):
    name: str = Field(default='Unknown-next', min_length=2, max_length=30)
