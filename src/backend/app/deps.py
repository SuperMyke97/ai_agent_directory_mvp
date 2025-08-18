from typing import Annotated
from .auth import verify_password
from .database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, InvalidTokenError
from .models.users import User
from .schemas import TokenData
from .auth import SECRET_KEY, ALGORITHM

session_dep = Annotated[Session, Depends(get_db)] 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_user(db: session_dep, username: str) -> User | None:
    user = db.query(User).filter(User.username == username).first()
    return user

def authenticate_user(db: session_dep, username: str, password: str)-> User | None:
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(plain_password=password, hashed_password=user.hash_password):
        return False
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: session_dep) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username == 'unknown':
            raise credentials_exception
        token_data = TokenData(username=username, is_admin=payload.get("is_admin", False))
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user