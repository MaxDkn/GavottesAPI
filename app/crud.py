from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import app.models as models, app.schemas as schemas


def get_house(db: Session, house_id: int):
    stored_house = db.query(models.House).filter(models.House.id == house_id).first()
    if not stored_house:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"House with ID {house_id} not found")    
    return stored_house
    

def get_houses(db: Session):
    return db.query(models.House).all()


def create_house(db: Session, house: schemas.HouseCreate):
    db_house = models.House(**house.dict())
    db.add(db_house)
    db.commit()
    db.refresh(db_house)
    return db_house


def modify_house(db: Session, house_id: int, house: schemas.House):
    stored_house_model = get_house(db=db, house_id=house_id)
    update_data = house.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(stored_house_model, key, value)
    db.commit()
    db.refresh(stored_house_model)
    return get_house(db=db, house_id=house_id)


def delete_house(db: Session, house_id: int):
    stored_house = get_house(db=db, house_id=house_id)
    db.delete(stored_house)
    db.commit()
    return {"msg": f"House {house_id} deleted without problems!"}
 