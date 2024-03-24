"""Exposed hardware classes and methods."""
from api.endpoints.hardware.cpu_endpoint import cpu_router
from api.endpoints.hardware.gpu_endpoint import gpu_router
from api.endpoints.hardware.ram_endpoint import ram_router
from fastapi import APIRouter

hardware_router = APIRouter(
    prefix="/hardware",
    tags=["Hardware"],
)

hardware_router.include_router(cpu_router)
hardware_router.include_router(gpu_router)
hardware_router.include_router(ram_router)
