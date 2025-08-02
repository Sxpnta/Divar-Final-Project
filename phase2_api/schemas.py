from pydantic import BaseModel 
from datetime import datetime
from typing import Optional

class AdBase(BaseModel):
    title: str
    price: Optional[str] = None 
    region: Optional[str] = None
    datetime:Optional[str] = None
    link: str 
    description: Optional[str] = None
    rooms: Optional[int] = None
    area: Optional[str] = None
    year_built:Optional[str] = None
    document_type:Optional[str] = None
    
class Ad(AdBase):
    id: int 
    
class Config:
        orm_mode = True 
        