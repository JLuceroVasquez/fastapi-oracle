from app.app_settings import get_settings
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends, HTTPException, status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

settings = get_settings()

def create_access_token(data: dict):

    data_copy = data.copy()

    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION_MINUTES)

    data_copy.update({"exp": expiration_time})

    token = jwt.encode(data_copy, algorithm=settings.ALGORITHM, key=settings.SECRET__KEY)

    return token

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):

    try:

        payload = jwt.decode(token, key=settings.SECRET__KEY, algorithms=settings.ALGORITHM)

        username: str = payload.get('username')

        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No se pudo validar credenciales", headers={"WWW-Authenticate" :"Bearer"})
        
    except JWTError:
       
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No se pudo validar credenciales", headers={"WWW-Authenticate" :"Bearer"})
    
    return username
    
