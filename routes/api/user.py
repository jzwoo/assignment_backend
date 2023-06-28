from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status, Depends
from helpers.auto_increment_id import get_next_sequence_value
from helpers.jwt_functions import verify_token
from helpers.password_checks import hash_password
from models.user import User
from config.db import db
from schemas.user import users_entity, user_entity

user = APIRouter()


@user.get('/api/v1/users')
async def get_all_users():
    return users_entity(db.users.find())


@user.get('/api/v1/users/{user_id}')
async def get_user_by_id(user_id: int):
    # should be only one result since id is unique
    retrieved_user = db.users.find_one({"user_id": user_id})
    if retrieved_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user_entity(retrieved_user)


@user.post('/api/v1/users', status_code=status.HTTP_201_CREATED)
async def create_user(new_user: User, requester=Depends(verify_token)):
    if requester['role'] != 'Admin':
        # forbidden
        raise HTTPException(status_code=403)

    if new_user.password is None or new_user.name is None:
        raise HTTPException(status_code=400, detail="Missing Parameters")

    # check for uniqueness of name
    retrieved_user = db.users.find_one({"name": new_user.name})
    if retrieved_user is not None:
        raise HTTPException(status_code=409, detail="Duplicate name")

    # default values for role and locked if not specified
    new_user.role = 'Viewer' if new_user.role is None else new_user.role
    new_user.locked = False if new_user.locked is None else new_user.locked
    # add time created
    new_user.date_of_creation = datetime.now(timezone.utc)
    # salt and hash password
    new_user.password = hash_password(new_user.password)
    # get auto incremented id
    new_user.user_id = get_next_sequence_value("user_id")

    db.users.insert_one(dict(new_user))
    return user_entity(dict(new_user))


@user.delete('/api/v1/users/{user_id}')
async def delete_user(user_id: int, requester=Depends(verify_token)):
    if requester['role'] != 'Admin':
        # forbidden
        raise HTTPException(status_code=403)

    query = {"user_id": user_id}
    retrieved_user = db.users.find_one(query)
    if retrieved_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.users.delete_one(query)
    return "User deleted"


@user.put('/api/v1/users/{user_id}')
async def update_user(user_id: int, updates: User, requester=Depends(verify_token)):
    if requester['role'] != 'Admin':
        # forbidden
        raise HTTPException(status_code=403)

    query = {"user_id": user_id}
    omitted_fields = ['name', 'password', 'user_id', 'date_of_creation']
    dict_updates = dict(updates)
    update_query = {
        "$set": {key: dict_updates[key] for key in dict_updates if
                 key not in omitted_fields and dict_updates[key] is not None}
    }
    db.users.update_one(query, update_query)

    retrieved_user = db.users.find_one(query)
    if retrieved_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user_entity(retrieved_user)
