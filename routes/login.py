from fastapi import APIRouter, HTTPException
from fastapi.security import HTTPBasicCredentials
from config.db import db
from helpers.jwt_functions import generate_jwt_token
from helpers.password_checks import verify_password
from schemas.user import user_entity

login = APIRouter()


@login.post('/login')
async def login_controller(credentials: HTTPBasicCredentials):
    name = credentials.username
    password = credentials.password
    user = db.users.find_one({'name': name})

    if user is None:
        raise HTTPException(status_code=401)

    if not verify_password(password, user['password']):
        raise HTTPException(status_code=401)

    token = generate_jwt_token(user_entity(user))
    return {"accessToken": token, "name": name}
