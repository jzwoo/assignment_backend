import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

load_dotenv()
SECRET_KEY = os.getenv('JWT_SECRET')


def generate_jwt_token(user):
    payload = {
        "name": user['name'],
        "role": user['role'],
        "user_id": user['user_id'],
        "iat": datetime.utcnow(),
        # 30 minutes expiration from current
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


security = HTTPBearer()


def verify_token(token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])

        user = {
            "name": payload['name'],
            "role": payload['role'],
            "user_id": payload['user_id'],
        }

        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
