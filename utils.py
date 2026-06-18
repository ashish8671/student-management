from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

ALGORITHM = "HS256"

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(
    password: str,
    hashed_pass: str
) -> bool:
    return password_context.verify(
        password,
        hashed_pass
    )


def create_access_token(
    subject: Union[str, Any]
) -> str:

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode = {
        "exp": expire,
        "sub": str(subject)
    }

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def create_refresh_token(
    subject: Union[str, Any]
) -> str:

    expire = datetime.utcnow() + timedelta(
        minutes=REFRESH_TOKEN_EXPIRE_MINUTES
    )

    to_encode = {
        "exp": expire,
        "sub": str(subject)
    }

    return jwt.encode(
        to_encode,
        REFRESH_SECRET_KEY,
        algorithm=ALGORITHM
    )