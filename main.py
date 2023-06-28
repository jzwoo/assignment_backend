from fastapi import FastAPI
from routes.login import login
from routes.api.user import user

app = FastAPI()

app.include_router(login)
app.include_router(user)
