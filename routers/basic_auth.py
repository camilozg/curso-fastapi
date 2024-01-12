from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

# Run server: uvicorn basic_auth:app --reload


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
    UserDB(username="naruto", disabled=False, password="123"),
    UserDB(username="edward", disabled=False, password="456"),
    UserDB(username="satoru", disabled=False, password="789"),
]


async def current_user(token: str = Depends(oauth2)):
    try:
        return next(user for user in users_list if user.username == token)
    except StopIteration:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authorized", {"WWW-Authenticate": "Bearer"})


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    try:
        user = next(user for user in users_db if user.username == form.username)
        if user.password != form.password or user.disabled:
            raise HTTPException(400, "User or password are not correct")
        return {"access_token": user.username, "token_type": "bearer"}
    except StopIteration:
        raise HTTPException(400, "User or password are not correct")


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
