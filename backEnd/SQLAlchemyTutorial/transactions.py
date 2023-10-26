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