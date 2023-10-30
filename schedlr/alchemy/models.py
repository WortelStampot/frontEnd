from __init__ import alchemyDB # will this work?

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class User(alchemyDB.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String)