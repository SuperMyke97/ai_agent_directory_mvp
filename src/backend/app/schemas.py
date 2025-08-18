from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

class UserUpdateSchema(BaseModel):
    full_name: str | None = None
    username: str | None = None
    email: EmailStr | None = None
    is_admin: bool | None = None
    

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    is_admin: bool | None = None

    class Config:
        from_attributes = True