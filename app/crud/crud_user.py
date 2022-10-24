import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from secrets import token_urlsafe
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserSchema
from app.config import settings


def _encrypt_password(password: str) -> str:
    # Warning: ECB mode always encrypt a message in the same way if the key is the same
    # But we cannot use other method, because we only have the api_key, so we don't know the user
    # And without the user, we would have to compare all the api_keys in the database with the given api_key
    key = hashlib.scrypt(settings.secret_key.encode(), salt=settings.salt.encode(), n=2**14, r=8, p=1, dklen=32)
    encryptor = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
    try:
        return base64.b64encode(encryptor.update(password.encode()) + encryptor.finalize()).decode()
    except ValueError:
        # This only happens when user write a short password, it doesn't happen in create_user
        return ''


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
