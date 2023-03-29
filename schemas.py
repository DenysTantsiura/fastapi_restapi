from datetime import date
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    name: str = Field('Unknown', min_length=2, max_length=30)
    last_name: str = Field('Unknown', min_length=2, max_length=40)
    email: EmailStr = EmailStr # str -> Field('Unknown@mail.com', min_length=6, max_length=30)  # i@i.ua
    phone: int = Field(000, gt=0, le=9999999999999999)
    birthday: date = Field(date)
    description = Field('-')  # String


class ContactResponse(ContactModel):
    id: int = 1

    class Config:
        orm_mode = True


class CatToNameModel(BaseModel):
    name: str = Field('Unknown', min_length=2, max_length=30)


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
