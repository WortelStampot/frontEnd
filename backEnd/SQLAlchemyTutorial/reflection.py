from start import engine

# Table Reflection
from sqlalchemy import text, Table, MetaData
metadata_object = MetaData()

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
# reflect it, and store the reflection on this 'metadata_object'
some_table = Table('some_table', metadata_object, autoload_with=engine)