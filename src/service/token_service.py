from jose import jwt, JWTError
from fastapi import Request, HTTPException, status

from src.schema.token_schema import Token
from datetime import datetime, timedelta
from src.config.hash import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM





def create_token(data: dict) -> Token:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES )
    to_encode.update({"exp": expire})
    return Token( access_token= jwt.encode(to_encode,
               SECRET_KEY,
               algorithm=ALGORITHM),
               token_type="Bearer")

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré"
        )  
