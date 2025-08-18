import os
import jwt
import pendulum

from pathlib import Path
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from dotenv import load_dotenv



load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


if SECRET_KEY is None:
    raise ValueError("SECRET_KEY environment variable is not set. Please set it to a secure random string.")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
    Verifies a plain-text password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Hashes a password using bcrypt.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: pendulum.Duration | None = None):
    """
    Creates a JWT access token with an expiration time.

    The function now uses pendulum for all datetime and timedelta operations,
    which automatically handles timezones correctly (UTC by default).
    """
    to_encode = data.copy()
    
    
    now = pendulum.now('UTC')
    
    if expires_delta:
        
        expire = now.add(
            years=expires_delta.years,
            months=expires_delta.months,
            weeks=expires_delta.weeks,
            days=expires_delta.days,
            hours=expires_delta.hours,
            minutes=expires_delta.minutes,
            seconds=expires_delta.seconds
        )
    else:
       
        expire = now.add(minutes=15)
    # Update the expiration time in the token data
    to_encode['iat'] = now.int_timestamp  # Add issued at time
    to_encode['exp'] = expire.int_timestamp  # pendulum uses int_timestamp for epoch
    to_encode['sub'] = data.get('sub', 'unknown')  # Ensure 'sub' is always present
    to_encode['is_admin'] = data.get('is_admin', False)  # Ensure 'is_admin' is always present
    # Encode the token using the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
