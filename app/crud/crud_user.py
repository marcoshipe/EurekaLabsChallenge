import base64
from secrets import token_urlsafe
from typing import Optional
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from app.models.user import User
from app.schemas.user import UserSchema
from app.config import settings


def _encrypt_password(password: str) -> str:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=settings.salt.encode(), iterations=390000)
    key = base64.urlsafe_b64encode(kdf.derive(settings.secret_key.encode()))
    return Fernet(key).encrypt(password.encode()).decode()


def get_user_by_apikey(db: Session, api_key: str) -> Optional[User]:
    return db.query(User).filter(User.hashed_api_key == _encrypt_password(api_key)).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserSchema) -> str:
    api_key = token_urlsafe(12)
    while get_user_by_apikey(db, api_key) is not None:
        api_key = token_urlsafe(12)
    db_user = User(name=user.name, last_name=user.last_name, email=user.email,
                   hashed_api_key=_encrypt_password(api_key))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return api_key
