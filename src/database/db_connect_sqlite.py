# підключення до бази даних (sqlite/PostgreSQL)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#!!!!!!!!!!!!!!!! PostgreSQL
# рядок з'єднання з базою даних (sqlite/PostgreSQL) за допомогою SQLAlchemy:
# SQLite to RAM: # engine = create_engine('sqlite:///:memory:', echo=True)
# https://www.sqlite.org/inmemorydb.html
# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  # "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "sqlite:////1/sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/my_db"
# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:123456@localhost:5432/my_app"

# створення двигуна
# для асинхронного використання різні користувачі повинні мати окремі потоки а не 1 і той самий 
engine = create_engine(  
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    ) # "check_same_thread": False - для SQLite сказати, щоб для з'єднання не використовувати 1 і той самий потік

# створення фабрики сесій, яка використовується для створення сесій для взаємодії 
# з базою даних. Фабрика SessionLocal налаштована так, 
# щоб не виконувати автокомміт та автоскидання сесії, і прив'язана до двигуна, створеного раніше:
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
''' False - дає можливість працювати з транзакціями, де можна виконувати кілька операцій і або 
підтвердити їх всі відразу commit, або відкотити rollback у разі помилки.

Параметр autocommit - це режим, коли кожна операція з базою даних автоматично підтверджується (комітиться). 
Тобто будь-які зміни, які ви вносите до бази даних, відразу ж стають активними і не можуть бути скасовані. 
За замовчуванням для роботи з SQLAlchemy увімкнено режим автокомміту.

Параметр autoflush - це режим, коли будь-які зміни, які ви вносите в об'єкти сесії, 
автоматично відправляються в базу даних. Іншими словами, будь-які зміни, які ви вносите в об'єкти, 
відразу ж стають активними і можуть бути помітні в базі даних. За замовчуванням для роботи 
з SQLAlchemy увімкнено режим автоскидання.
'''

Base = declarative_base()


# Dependency - ін'єкція
def get_db():
    """Returns a session using a factory: SessionLocal."""  
    db = SessionLocal()
    try:
        yield db
    finally: # Сесія закривається при виході з функції з використанням блоку finally.
        db.close()
