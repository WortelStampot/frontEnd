from sqlalchemy.orm import DeclarativeBase

# Establishing a Declarative Base
class Base(DeclarativeBase):
    pass


# Declaring Mapped Classes
from typing import List, Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = 'user_account'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    addresses: Mapped[List['Address']] = relationship(back_populates='user')

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})'
    
class Address(Base):
    __tablename__ = 'address'

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey('user_account.id'))

    user: Mapped[User] = relationship(back_populates='addresses')

    def __repr__(self) -> str:
        return f'Address(id={self.id!r}), email_address={self.email_address!r}'
    
# Emitting DDL to the database from ORM mapping
from start import engine

Base.metadata.create_all(engine)

'''
BEGIN (implicit)
...

CREATE TABLE user_account (
        id INTEGER NOT NULL, 
        name VARCHAR(30) NOT NULL, 
        fullname VARCHAR, 
        PRIMARY KEY (id)
)

CREATE TABLE address (
        id INTEGER NOT NULL, 
        email_address VARCHAR NOT NULL, 
        user_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(user_id) REFERENCES user_account (id)
)

...
COMMIT
'''


# Table Reflection
from sqlalchemy import text, Table

# create 'some_table' to reflect
def commitChanges():
    with engine.connect() as conn:
        conn.execute(
            text("CREATE TABLE some_table (x int, y int)") #create table
            )
        conn.execute(
            text("INSERT INTO some_table (x,y) VALUES (:x, :y)"), # insert values into table
            [{"x":1, "y":1}, {"x":2, "y":4}] #where these are the values for :x, :y 
        )
        conn.commit()

commitChanges()

# passing 'engine' to autoload_with says:
# in this engine's database, look for a table named 'some_table',
# reflect it, and store the reflection on this 'Base.metadata' MetaData object
some_table = Table('some_table', Base.metadata, autoload_with=engine)