from jose import jwt,JWTError
from datetime import datetime, timedelta
from pwdlib import PasswordHash
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_access_token(data: dict):
    to_encode=data.copy()

    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def verify_token(token: str):
    try:
        payload=jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])

        username=payload.get("sub")

        if username is None:
            return None
        return username
    
    except JWTError:
        return None

password_hash = PasswordHash.recommended()

def hash_password(password: str):
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(
        plain_password,
        hashed_password
    )