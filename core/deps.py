from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from core.jwt import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

fake_users_db = []  # временно


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401)

        user = next((u for u in fake_users_db if u["email"] == email), None)

        if user is None:
            raise HTTPException(status_code=401)

        return user

    except JWTError:
        raise HTTPException(status_code=401)
