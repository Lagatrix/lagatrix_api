"""Main module for the API REST application."""
from fastapi import FastAPI

from api import user_router, group_router, crontab_router, storage_router

app = FastAPI()

app.include_router(user_router)
app.include_router(group_router)
app.include_router(crontab_router)
app.include_router(storage_router)
