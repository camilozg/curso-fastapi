from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int


class UserResponse(User):
    sent_to_user: List[int] = []


users_list = [
    User(id=1, name="Naruto", surname="Uzumaki", age=17),
    User(id=2, name="Edward", surname="Elric", age=15),
    User(id=3, name="Satoru", surname="Gojo", age=28),
]


@router.get("/", response_model=List[User])
async def get_all_users():
    return users_list


@router.get("/query", response_model=User)
async def get_user_by_query(id: int):
    try:
        return [user for user in users_list if user.id == id][0]
    except IndexError:
        raise HTTPException(404, "User not found")


@router.get("/{id}", response_model=User)
async def get_user(id: int):
    try:
        return [user for user in users_list if user.id == id][0]
    except IndexError:
        raise HTTPException(404, "User not found")


@router.post("/", response_model=User, status_code=201)
async def create_user(request_user: User):
    if len([user for user in users_list if user.id == request_user.id]) > 0:
        raise HTTPException(400, "User already exists")
    else:
        users_list.append(request_user)
        return request_user


@router.put("/", response_model=User)
async def update_user(request_user: User):
    try:
        user_index = next(index for index, user in enumerate(users_list) if user.id == request_user.id)
        users_list[user_index] = request_user
        return users_list[user_index]
    except StopIteration:
        raise HTTPException(404, "User not found")


@router.delete("/{id}", response_model=User)
async def delete_user(id: int):
    try:
        user_index = next(index for index, user in enumerate(users_list) if user.id == id)
        user_deleted = users_list.pop(user_index)
        return user_deleted
    except StopIteration:
        raise HTTPException(404, "User not found")
