"""This module contains the GPU endpoint for the API REST."""
from typing import Annotated

from gpu_lib import GpuManager, Gpu, DriverNotFound, NotValidGpuError
from fastapi import APIRouter, Security, HTTPException
from shell_executor_lib import CommandManager, CommandError
from starlette import status

from api.dependencies import auth_user

gpu_router = APIRouter(
    prefix="/gpu",
    tags=["GPU"],
)


@gpu_router.get(
    path="",
    response_model=Gpu,
    response_description="Returns all the information of the GPU.",
    status_code=200
)
async def get_gpu(command_manager: Annotated[CommandManager, Security(auth_user)]) -> Gpu:
    """Get the GPU information.

    Args:
        command_manager: To execute commands in the shell.

    Returns:
        The GPU information.

    Raises:
        HTTP Error 422: If the GPU is not supported or the driver is not installed.
        HTTP Error 500: If there is an error in the command manager.
    """
    try:
        return await (await GpuManager.init(command_manager)).get_gpu()
    except NotValidGpuError as not_valid_gpu:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(not_valid_gpu))
    except DriverNotFound as driver_not_found:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(driver_not_found))
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))


@gpu_router.get(
    path="/use",
    response_model=float,
    response_description="Returns the use of GPU.",
    status_code=200
)
async def get_gpu_use(command_manager: Annotated[CommandManager, Security(auth_user)]) -> float:
    """Get the GPU use.

    Args:
        command_manager: To execute commands in the shell.

    Returns:
        The GPU use.

    Raises:
        HTTP Error 422: If the GPU is not supported or the driver is not installed.
        HTTP Error 500: If there is an error in the command manager.
    """
    try:
        return await (await GpuManager.init(command_manager)).get_use()
    except NotValidGpuError as not_valid_gpu:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(not_valid_gpu))
    except DriverNotFound as driver_not_found:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(driver_not_found))
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))


@gpu_router.get(
    path="/temperature",
    response_model=float,
    response_description="Returns the temperature of the GPU.",
    status_code=200
)
async def get_gpu_temperature(command_manager: Annotated[CommandManager, Security(auth_user)]) -> float:
    """Get the GPU temperature.

    Args:
        command_manager: To execute commands in the shell.

    Returns:
        The GPU temperature.

    Raises:
        HTTP Error 422: If the GPU is not supported or the driver is not installed.
        HTTP Error 500: If there is an error in the command manager.
    """
    try:
        return await (await GpuManager.init(command_manager)).get_temperature()
    except NotValidGpuError as not_valid_gpu:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(not_valid_gpu))
    except DriverNotFound as driver_not_found:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(driver_not_found))
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))
