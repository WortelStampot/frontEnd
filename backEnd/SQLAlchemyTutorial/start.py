from sqlalchemy import create_engine
local_db = 'backEnd/SQLAlchemyTutorial/tutorial.sqlite'
mem_db = ':memory:'

engine = create_engine(f"sqlite+pysqlite:///{mem_db}", echo=True)