from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.user import UserSchema
from app.crud.crud_user import get_user_by_email, create_user


router = APIRouter(prefix='/users', tags=['Users'])


responses = {
    200: {
        'description': 'Successful Response',
        'content': {'application/json': {'example': {'api_key': 'TEST_API_KEY'}}}
    },
    400: {
        'description': 'Error: Bad Request',
        'content': {'application/json': {'example': {'detail': 'Email already registered'}}}
    },
}


@router.post('/', responses=responses, summary='Create User')
def create_user_api(user: UserSchema, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    return {'api_key': create_user(db=db, user=user)}
