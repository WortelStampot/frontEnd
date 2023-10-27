from start import engine
"""
the foundation for these SQL queries are Python objects
that represent database concepts like tables and columns.
These objects are known collectively as database metadata
"""
from sqlalchemy import MetaData, Table, Column, Integer, String

# -- Setting up Metadata --
'''
a MetaData object will hold our collection of Table objects
one MetaData object for the entire progarm is common
'''
metadata_obj = MetaData()

# -- Table Objects --
user_table = Table(
    'user_account',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String(30)),
    Column('fullname', String)
)

# the collection of a Table's Columns are usually accessed with:
user_table.c 
# this returns:
# <sqlalchemy.sql.base.ReadOnlyColumnCollection object at 0x103c5bdd0>

# exmaple:
user_table.c.fullname
# returns the 'fullname' Column defined above:
# Column('fullname', String(), table=<user_account>)


# -- Declaring Simple Constraints --
from sqlalchemy import ForeignKey

address_table = Table( "address", metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('user_id', ForeignKey('user_account.id'), nullable=False),
    Column('email_address', String, nullable=False)
)

# Primary Keys
# the primary key of a table is usually set 'implicitly' with the argument
# primary_key= True

# we can see the result with:
address_table.primary_key
    # returning the initiated PrimaryKeyConstraint object
    # PrimaryKeyConstraint(Column('id', Integer(), table=<address>, primary_key=True, nullable=False))

# Foreign Keys
# a foreign key referencing a single column of another table
# are usually set with passing in the ForeignKey object
# which constructs a ForeignKeyConstraint

    # a foreign key referencing multiple columns is possible
    # then, the ForeignKeyConstraint object is passed in directly


# -- Emitting DDL to the Database --
'''
DDL: Data Definition Language a subset of SQL
used to configure tables, constraints,
and other perminante objects of a database schema
'''

# We now have the structure for a database with two tables:
user_table # with columns 'id', 'name', 'fullname'
address_table # with columns 'id', 'user_id', 'email_address'

metadata_obj # holds the two tables
engine # holds our sql database address

# to insert rows and query data,
# we first build the structure:
metadata_obj.create_all(engine)

'''
BEGIN (implicit)
...

CREATE TABLE user_account (
        id INTEGER NOT NULL, 
        name VARCHAR(30), 
        fullname VARCHAR, 
        PRIMARY KEY (id)
)

CREATE TABLE address (
        id INTEGER NOT NULL, 
        user_id INTEGER NOT NULL, 
        email_address VARCHAR NOT NULL, 
        PRIMARY KEY (id), 
        FOREIGN KEY(user_id) REFERENCES user_account (id)
)

...
COMMIT
'''

# the create process takes care of emitting CREATE statements in the correct order
# MetaData also have a .drop_all() method which emits DROP statements in the reverse