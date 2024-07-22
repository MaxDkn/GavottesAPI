from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from app import crud, models, schemas
from app.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/get_houses")
async def get_all_houses(db: Session = Depends(get_db)):
    return crud.get_houses(db=db)


@app.get("/api/get_house/{house_id}", response_model=schemas.HouseResponse)
async def get_house(house_id: int, db: Session = Depends(get_db)):
    return crud.get_house(db=db, house_id=house_id)


@app.post("/api/create_house/", response_model=schemas.HouseResponse)
async def create_house(house: schemas.HouseCreate, db: Session = Depends(get_db)):
    return crud.create_house(db=db, house=house)


@app.patch("/api/update_house/{house_id}") #, response_model=schemas.HouseResponse)
async def modify_house(house_id: int, house: schemas.HouseUpdate, db: Session = Depends(get_db)):
    return crud.modify_house(db=db, house_id=house_id, house=house)


@app.delete("/api/delete_house/{house_id}")
async def delete_house(house_id: int, db: Session = Depends(get_db)):
    return crud.delete_house(db=db, house_id=house_id)
