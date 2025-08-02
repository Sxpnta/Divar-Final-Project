from sqlalchemy.orm import Session 
from phase1_crawler.models import DivarAd 
from typing import Optional
from sqlalchemy import func 

def get_ads(db: Session, skip: int = 0, limit: int = 10, region: Optional[str] = None, rooms: Optional[int] = None):
    query = db.query(DivarAd)

    if region: 
        query = query.filter(func.lower(DivarAd.region).contains(region.lower()))
    if rooms is not None:
        query = query.filter(DivarAd.rooms == rooms)
        
    return query.order_by(DivarAd.posted_date.desc()).offset(skip).limit(limit).all()

def get_ad(db: Session, ad_id: int):
    return db.query(DivarAd).filter(DivarAd.id == ad_id).first()

