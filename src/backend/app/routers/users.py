from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from backend.app.schemas import UserSchema, Token
from backend.app.models.users import User
from backend.app.auth import get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from backend.app.deps import get_current_user, authenticate_user, session_dep
import pendulum


router = APIRouter(
    prefix="/users",
    tags=["users_authentication"],
    responses={404: {"description": "Not found"}},
)




@router.post("/signup", response_model=Token)
async def signup(
    user: UserSchema,
    db: session_dep,
):
    """
    User signup endpoint.
    """
    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        hash_password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = create_access_token(data={"sub": new_user.username,"is_admin": new_user.is_admin})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: session_dep,
):
    """
    User login endpoint.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = pendulum.Duration(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username, "is_admin": user.is_admin}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Get the current logged-in user.
    """
    return current_user