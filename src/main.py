"""Main module for the API REST application."""
from fastapi import FastAPI

from api import user_router

app = FastAPI()

app.include_router(user_router)
