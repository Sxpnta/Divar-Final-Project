import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from fastapi import FastAPI, Depends, HTTPException , Query
from sqlalchemy.orm import Session 
from phase1_crawler.database import SessionLocal 
from . import crud, schemas 
from phase1_crawler import models
from typing import List, Optional

app = FastAPI()

#Depend DB session 
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

@app.get("/",include_in_schema=False)
def read_root():
    return {"message":"Welcome to the Divar Ad API. Use /ads or /ads{ad_id} for data."}

@app.get("/ads", response_model=List[schemas.Ad])
def read_ads(
    skip: int = 0, 
    limit: int = 10, 
    region: Optional[str] = Query(None, description="Filter by region"),
    rooms: Optional[int] = Query(None, description="Filer by number of rooms"),
    db: Session = Depends(get_db)
):  
    try:
        return crud.get_ads(db, skip=skip , limit=limit, region=region, rooms=rooms)
    except Exception as e:
        print(f"Exception in /ads: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/ads/{ad_id}", response_model=schemas.Ad)
def read_ad(ad_id: int , db: Session = Depends(get_db)):
    try:
        db_ad= crud.get_ad(db, ad_id)
        if db_ad is None:
            raise HTTPException(status_code=404, detail="Ad not found")
        return db_ad
    except Exception as e:
        print(f"Exception in /ads/{ad_id}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    