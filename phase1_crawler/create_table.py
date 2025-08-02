from .database import engine, Base 
from . import models 

try:
    Base.metadata.create_all(bind=engine)
    print("Table created")
except Exception as e:
    print(f"Failed to create table: {e}")
    
