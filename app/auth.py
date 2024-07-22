from passlib.context import CryptContext
from fastapi import HTTPException, status
import app.models as models, app.schemas as schemas
from sqlalchemy.orm import Session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt algorithm."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a given hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db: Session, username: str):
    stored_user = db.query(models.User).filter(models.User.username==username)
    """if not stored_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with "username" {username} not found')
    """
    return stored_user
