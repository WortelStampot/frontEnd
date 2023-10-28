from start import engine
from metadata_core import user_table, address_table
from metadata_orm import User, Address

import data_insert # run the insert statements to fill the database

# -- The select() Construct --
from sqlalchemy import select

statement = select(user_table).where(user_table.c.name == 'spongebob')
'''
SELECT user_account.id, user_account.name, user_account.fullname 
FROM user_account 
WHERE user_account.name = :name_1
'''

# -- with core
with engine.connect() as connection:
   for row in connection.execute(statement):
      print(row)
" (1, 'spongebob', 'Spongebob Squarepants') "

# -- with ORM
from sqlalchemy.orm import Session
statementORM = select(User).where(User.name == 'spongebob')

with Session(engine) as session:
   for row in session.execute(statementORM):
      print(row)
" (User(id=1, name='spongebob', fullname='Spongebob Squarepants'),) "


# -- Setting the COLUMNS and FROM clause --
select((user_table))
'''
SELECT user_account.id, user_account.name, user_account.fullname 
FROM user_account
'''

# when executing 'select( (user_table) )' with the ORM approach there is an important difference:
# since we'd be selecting a 'full entity' like a User instance,
# the User object is returned as a 'single element' in the returning rows

row = session.execute(select(User)).first()
"(User(id=1, name='spongebob', fullname='Spongebob Squarepants'),)"

#this row has one element
row[0]
"User(id=1, name='spongebob', fullname='Spongebob Squarepants')"

# -- a ScalarResult
user = session.scalars(select(User)).first()
"User(id=1, name='spongebob', fullname='Spongebob Squarepants')"

# alternatively, we can select individual elements of an ORM object
# by using the class attributes
select(User.name, User.fullname)
'''
SELECT user_account.name, user_account.fullname 
FROM user_account
'''

row = session.execute(
   select(User.name, User.fullname),
).first()
"('spongebob', 'Spongebob Squarepants')"

# the approaches can be mixed:

result = session.execute(
   select(User.name, Address)
   .where(User.id == Address.id).order_by(Address.id)
).all()
'''
[('spongebob', Address(id=1), email_address='spongebob@sqlalchemy.org'),
('sandy', Address(id=2), email_address='sandy@sqlalchemy.org'),
('patrick', Address(id=3), email_address='sandy@squirrelpower.org')]
'''

# -- Selecting from Labeled SQL Expressions --
from sqlalchemy import func, cast
statement = select(
   ('Username: ' + user_table.c.name).label('username'),
).order_by(user_table.c.name)

with engine.connect() as connection:
   for row in connection.execute(statement):
      print(row.username) # making use of the label in the result
'''
Username: patrick
Username: sandy
Username: spongebob
'''

# -- Selecting with Textual Column Expressions --
from sqlalchemy import text
statement = select(
   text(" 'some phrase' "),
   user_table.c.name,
   ).order_by(user_table.c.name)

with engine.connect() as connection:
   result = connection.execute(statement)
   print( result.all() )
'''
[('some phrase', 'patrick'),('some phrase', 'sandy'), ('some phrase', 'spongebob')]
'''

# -- using literal_column()
from sqlalchemy import literal_column
statement = select(
   literal_column(" 'their phrase' ").label('p'),
   user_table.c.name,
).order_by(user_table.c.name)

with engine.connect() as connection:
   for row in connection.execute(statement):
      print(f'{row.p}, {row.name}')
'''
their phrase, patrick
their phrase, sandy
their phrase, spongebob
'''

# -- the WHERE clause --
user_table.c.name == 'squidward'
" user_account.name = :name_1 "

address_table.c.user_id > 10
" address.user_id > :user_id_1 "

# we can use expressions containing the ==, >, <, !=... etc operators
# to create WHERE clauses, when passing these expressions to Select.where() method

select(user_table).where(user_table.c.name == 'squidward')
'''
SELECT user_account.id, user_account.name, user_account.fullname 
FROM user_account 
WHERE user_account.name = :name_1
'''

# to produce multiple expressions joined by AND,
# select.where() can be invoked multiple times

select(address_table.c.email_address)\
   .where(user_table.c.name == 'squidward')\
   .where(address_table.c.user_id == user_table.c.id)
'''
SELECT address.email_address 
FROM address, user_account 
WHERE user_account.name = :name_1 AND address.user_id = user_account.id
'''

# Select.where() also accepts multiple arguments
select(address_table.c.email_address).where(
   user_table.c.name == 'squidward',
   address_table.c.user_id == user_table.c.id,
)
'''
SELECT address.email_address 
FROM address, user_account 
WHERE user_account.name = :name_1 AND address.user_id = user_account.id
'''

# 'AND' and 'OR' conjunctions are available direct with and_() and or_() functions
from sqlalchemy import and_, or_

select(Address.email_address).where(
   and_(
      or_(User.name == 'squidward', User.name == 'sandy'),
      Address.user_id == User.id,
   )
)
'''
SELECT address.email_address 
FROM address, user_account 
WHERE (user_account.name = :name_1 OR user_account.name = :name_2)
AND address.user_id = user_account.id
'''

# -- Select.filter_by()
select(User).filter_by(name='spongebob', fullname='Spongebob Squarepants')
'''
SELECT user_account.id, user_account.name, user_account.fullname 
FROM user_account 
WHERE user_account.name = :name_1 AND user_account.fullname = :fullname_1
'''

# -- Explicit FROM clauses and JOINs --
