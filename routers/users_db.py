from typing import List

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from db.client import db_client
from db.models.user import User
from db.schemas.user import user_schema, users_schema

router = APIRouter(
    prefix="/usersdb",
    tags=["usersdb"],
)


users_list = []


@router.get("/", response_model=List[User])
async def get_all_users():
    return users_schema(db_client.users.find())


@router.get("/{id}", response_model=User)
async def get_user(id: str):
    try:
        if db_client.users.find_one({"_id": ObjectId(id)}) is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "User not found")

        user = user_schema(db_client.users.find_one({"_id": ObjectId(id)}))

        return User(**user)
    except Exception:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User not found")


@router.post("/", response_model=User, status_code=201)
async def create_user(user: User):
    if db_client.users.find_one({"email": user.email}) is None:
        user_dict = dict(user)
        del user_dict["id"]

        object_id = db_client.users.insert_one(user_dict).inserted_id
        inserted_user = user_schema(db_client.users.find_one({"_id": object_id}))

        return User(**inserted_user)

    raise HTTPException(status.HTTP_400_BAD_REQUEST, "User already exists")


@router.put("/")
async def update_user(user: User):
    try:
        user_dict = dict(user)
        del user_dict["id"]
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)

    except Exception:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User not updated")


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_user(id: str):
    try:
        found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

        if not found:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "User not found")

    except Exception:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User not found")
