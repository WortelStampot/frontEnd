from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase 

class Base(DeclarativeBase):
    pass

alchemyDB = SQLAlchemy(model_class=Base)

# set up a database model
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class User(alchemyDB.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String)

class Role(alchemyDB.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    day: Mapped[str] = mapped_column(String, nullable=False)
    # callTime: Mapped[object] = do we store a datetime object directly?


# Question about this User class,
    # in the context of the scheduler, there's a Staff class with several methods,
    # would we add methods to this 'Users model'?
