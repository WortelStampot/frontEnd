from start import engine
from metadata_core import metadata_obj, user_table, address_table


# -- Using INSERT Statements --
from sqlalchemy import insert

statement = insert(user_table).values(
    name='spongebob', fullname='Spongebob Squarepants'
)
# print(statement) returns:
    # INSERT INTO user_account (name, fullname) VALUES (:name, :fullname)

# that insert function creates an Insert object,
# that SQL string comes from a 'Compiled' form of the Insert object,
# which contains a database specific SQL representation of the statement

# we can see this with
compiled = statement.compile()

# the parameters of our Insert construct can be seen here as well
# print(compiled.params) returns:
    # {'name': 'spongebob', 'fullname': 'Spongebob Squarepants'}


# -- Executing the Statement --
with engine.connect() as connection:
    result = connection.execute(statement)
    connection.commit()

# we've inserted a row into our 'user_account' table

# our statement above made use of the .values() method,
# to explicity create the VALUES clause 'VALUES (:name, :fullname)'
# where :name, and :fullname match the values of our passed in strings


# -- Insert usually generates the 'VALUES' clause automatically --

# when we don't use Insert.values(),
# we get an INSERT for every column on the table

insert(user_table)
# print( insert(user_table) ) returns:
    # INSERT INTO user_account (id, name, fullname) VALUES (:id, :name, :fullname)

# usually, insert() is used this way.
with engine.connect() as connection:
    connection.execute(
        insert(user_table),
        [
            {'name': 'sandy', 'fullname': 'Sandy Cheeks'},
            {'name': 'patrick', 'fullname': 'Patrick Star'}
        ]
    )
    connection.commit()

# -- Deep Alchemy --
from sqlalchemy import select, bindparam
scalar_subq = (
    select(user_table.c.id)
    .where(user_table.c.name == bindparam('username'))
    .scalar_subquery()
)

with engine.connect() as connection:
    result = connection.execute(
        insert(address_table).values(user_id=scalar_subq),
        [
            {'username': 'spongebob', 'email_address': 'spongebob@sqlalchemy.org'},
            {'username': 'sandy', 'email_address': 'sandy@sqlalchemy.org'},
            {'username': 'sandy', 'email_address': 'sandy@squirrelpower.org'},
        ], #NOTE: the trailing comma is helpful for 'git diff' with multi-line arguments
        # https://stackoverflow.com/a/17492103
    )
    connection.commit()

# -- an 'empty' INSERT --
# leaving the .values() method empty produces an INSERT of DEFAULT VALUES
insert(user_table).values().compile(engine)
'INSERT INTO user_account DEFAULT VALUES'


# -- INSERT...RETURNING --
insert(address_table).returning(
    address_table.c.id, address_table.c.email_address,
)
'''
INSERT INTO address (id, user_id, email_address) VALUES (:id, :user_id, :email_address)
RETURNING address.id, address.email_address
'''

# -- INSERT...FROM SELECT --
select_statement = select(user_table.c.id, user_table.c.name + '@aol.com')
insert(address_table).from_select(
    ['user_id', 'email_address'], select_statement,
)
'''
INSERT INTO address (user_id, email_address)
SELECT user_account.id, user_account.name || :name_1 AS anon_1 
FROM user_account
'''

