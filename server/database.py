import databases
from server.config import get_settings
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = get_settings().db_url
print(f'DATABASE_URL {DATABASE_URL}')
database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

DBBase = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        print(Exception)
        db.rollback()
    finally:
        db.close()

def create_db(db, value):
    db.add(value)
    db.commit()
    db.refresh(value)
    return value