from start import engine
from sqlalchemy import text

# Getting a Connecion
def getConnection():
    with engine.connect() as conn:
        result = conn.execute(text("select 'hello world'"))
        print(result.all())


# Commiting Changes
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

def beginOnce():
    with engine.begin() as connection:
        connection.execute(
            text('INSERT INTO some_table (x, y) VALUES (:x, :y)'),
            [{"x":6, "y":8}, {"x":9, "y":10}]
        )

commitChanges()
beginOnce()


# Basics of Statement Execution
def fetchRows(accessMethod):
    with engine.connect() as connection:
        result = connection.execute(
            text('SELECT x,y FROM some_table')
        )
        print(f'accessed with {accessMethod.__name__}')
        accessMethod(result)
        
def tupleAssignment(result):
    for x, y in result:
        print(f'x: {x} y: {y}')

def integerIndex(result):
    for row in result:
        x = row[0]
        y = row[1]
        print(f'x: {x} y: {y}')
        
def attributeName(result):
    for row in result:
        x = row.x
        y = row.y
        print(f'x: {x} y: {y}')

def mappingAccess(result):
    for dict_row in result.mappings():
        x = dict_row['x']
        y = dict_row['y']
        print(f'x: {x} y: {y}')

fetchRows(tupleAssignment)


# Sending Parameters
def sendParameters():
    with engine.connect() as connection:
        result = connection.execute(
            text('SELECT x,y FROM some_table WHERE y > :y'),
            {'y': 2} #dict sets the value for ':y'
        )
        for row in result:
            print(f'x: {row.x} y: {row.y}')

sendParameters()

def sendMultipleParameters():
    '''
    the SQL statement is invoked multiple times,
    once for each parameter dictionary
    '''
    with engine.connect() as connection:
        connection.execute(
            text('INSERT INTO some_table (x, y) VALUES (:x, :y)'),
            [   {'x': 11, 'y': 12}, {'x': 13, 'y':14}   ]
        )
        connection.commit()

sendMultipleParameters()


# Executing with an ORM Session
from sqlalchemy.orm import Session

def withSession():
    statement = text('SELECT x,y FROM some_table WHERE y> :y ORDER BY x, y')
    with Session(engine) as session:
        result = session.execute(statement, {'y':6})
        for row in result:
            print(f'x: {row.x} y: {row.y}')

withSession()

def sessionUpdate():
    with Session(engine) as session:
        result = session.execute(
            text('UPDATE some_table SET y= :y WHERE x= :x'),
            [ {'x': 9, 'y': 11}, {'x': 13, 'y': 15} ]
        )
        session.commit()

sessionUpdate()