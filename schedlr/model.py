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

class Staff(alchemyDB.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    availability: Mapped[str] # how to store this? dict value?
    # availability table with columns: staff Id, Monday, Tuesday, Wednesday, Thursday... ?

    rolePreference: Mapped[str] # list of Role Id's from Role table?
    # how do the Role Id's get referenced?

class Role(alchemyDB.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    callTime: Mapped[str] = mapped_column(String, nullable=False)
    qualifiedStaff: Mapped[str] = mapped_column(String, nullable=True) # Ids from staff table?
    perferredStaff: Mapped[str] = mapped_column(String, nullable=True) # reference to Staff table?