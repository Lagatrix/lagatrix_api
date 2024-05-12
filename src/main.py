"""Main module for the API REST application."""
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import user_router, group_router, crontab_router, storage_router, host_router, hardware_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(group_router)
app.include_router(crontab_router)
app.include_router(storage_router)
app.include_router(host_router)
app.include_router(hardware_router)
