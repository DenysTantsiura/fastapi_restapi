from sqlalchemy import Column, Date, Integer, String
# from sqlalchemy.orm import relationship

from src.database.db_connect import Base


class Contact(Base):
    __tablename__: str = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), index=True)
    last_name = Column(String(40), index=True)
    email = Column(String(30), unique=True, index=True)
    phone = Column(Integer, unique=True, index=True)
    birthday = Column(Date, index=True)
    description = Column(String(3000))
