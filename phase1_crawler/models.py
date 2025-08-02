from sqlalchemy import Column , Integer , String , DateTime , Text 
from .database import Base 

class DivarAd(Base):
    __tablename__ = "divar_ads" 
    id = Column(Integer, primary_key=True , index=True)
    title = Column(String(255), nullable=False)
    price = Column(String(100), nullable=True)
    region = Column(String(100), nullable=True)
    posted_date = Column(DateTime, nullable=True)
    link = Column(String(255) , unique=True, nullable=False )
    description = Column(Text, nullable=True)
    rooms = Column(Integer, nullable=True,)
    area = Column(String(50), nullable=True)
    year_built = Column(String(50), nullable=True)
    document_type = Column(String(50), nullable=True)
    
    def __repr__(self):
        return f"<DivarAd(title={self.title}, price={self.price}, region={self.region})>"
    
    