from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# the address of the database
SQL_DB_URL = "sqlite:///./school.db"

# the way to talk to the SQL
engine = create_engine(SQL_DB_URL, connect_args= {"check_same_thread": False})

# creates connections to the server
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# all ORM models will inherit from the class - Base
Base = declarative_base()


# used to connect to the database from our methods, when finished using it, the method closes the connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()