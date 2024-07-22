from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from app import crud, models, schemas, auth
from app.database import SessionLocal, engine
from typing import Annotated


models.Base.metadata.create_all(bind=engine)


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def decode(token, db: Session = Depends(get_db)):
    user = auth.get_user(db=db, username=token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: Annotated[schemas.User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = auth.get_user(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = auth.hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_user(current_user: Annotated[schemas.User, Depends(get_current_active_user)]):
    return current_user


@app.get("/api/get_houses")
async def get_all_houses(db: Session = Depends(get_db)):
    return crud.get_houses(db=db)


@app.post("/api/create_house/", response_model=schemas.HouseResponse)
async def create_house(house: schemas.HouseCreate, db: Session = Depends(get_db)):
    return crud.create_house(db=db, house=house)


@app.get("/api/get_house/{house_id}", response_model=schemas.HouseResponse)
async def read_house(house_id: int, db: Session = Depends(get_db)):
    return crud.get_house(db=db, house_id=house_id)


@app.patch("/api/update_house/{house_id}") #, response_model=schemas.HouseResponse)
async def update_house(house_id: int, house: schemas.HouseUpdate, db: Session = Depends(get_db)):
    return crud.modify_house(db=db, house_id=house_id, house=house)


@app.delete("/api/delete_house/{house_id}")
async def delete_house(house_id: int, db: Session = Depends(get_db)):
    return crud.delete_house(db=db, house_id=house_id)
