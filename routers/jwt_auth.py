from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run: openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="/login")
crypt = CryptContext(schemes=["bcrypt"])

# Install python-jose to generate and verify the JWT: pip install "python-jose[cryptography]"
# Install PassLib to handle password hashes: pip install "passlib[bcrypt]"
# Run server: uvicorn jwt_auth:app --reload


class User(BaseModel):
    username: str
    disabled: bool


class UserDB(User):
    password: str


users_list = [
    User(username="naruto", disabled=False),
    User(username="edward", disabled=False),
    User(username="satoru", disabled=False),
]

users_db = [
    UserDB(username="naruto", disabled=False, password="$2a$12$by7RxnFA5jheha5qIHDr/ur0uPd9KOn1E8nCKtSxANMPtlMIfBC46"),
    UserDB(username="edward", disabled=False, password="$2a$12$1xry/KYkYaw8GBZq062F3.LVu6Ge8UEwCB6Cutd4/t6yRE5omcl5i"),
    UserDB(username="satoru", disabled=False, password="$2a$12$aDdKS5Hp6/hBg0ElbFl5XukcsApbFuvjuIckSra.DVGZKgniEnoS6"),
]


async def auth_user(token: str = Depends(oauth2)):
    try:
        username = jwt.decode(token, SECRET_KEY, ALGORITHM).get("sub")
        user = next(user for user in users_list if user.username == username)
        return user

    except (JWTError, StopIteration):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authorized", {"WWW-Authenticate": "Bearer"})


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    try:
        user = next(user for user in users_db if user.username == form.username)

        if not crypt.verify(form.password, user.password) or user.disabled:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "User or password are not correct")

        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = {"sub": user.username, "exp": expire}

        return {"access_token": jwt.encode(access_token, SECRET_KEY, ALGORITHM), "token_type": "bearer"}

    except StopIteration:
        raise HTTPException(400, "User or password are not correct")


@router.get("/users/me")
async def me(user: User = Depends(auth_user)):
    return user
