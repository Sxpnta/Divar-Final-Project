from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
import os 
from dotenv import load_dotenv

load_dotenv()
DB_USER =os.getenv("DB_USER","postgres")
DB_PASSWORD =os.getenv("DB_PASSWORD","1234")
DB_HOST =os.getenv("DB_HOST", "localhost")
DB_PORT =os.getenv("DB_PORT", "5432")
DB_NAME=os.getenv("DB_NAME","divar_db")

database_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
try:        
        engine = create_engine(database_URL)
        engine.connect()
except OperationalError as e:
    raise Exception(f"Database connection failed: {e}")

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    




         