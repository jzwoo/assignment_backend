from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.allowedOrigins import allowedOrigins
from routes.login import login
from routes.api.user import user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowedOrigins,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(login)
app.include_router(user)
