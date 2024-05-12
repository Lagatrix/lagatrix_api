"""This module contains the CPU endpoint for the API REST."""
from typing import Annotated

from cpu_lib import CpuManager, Cpu
from fastapi import APIRouter, Security, HTTPException
from shell_executor_lib import CommandManager, CommandError
from starlette import status

from api.dependencies import auth_user

cpu_router = APIRouter(
    prefix="/cpu",
    tags=["CPU"],
)


@cpu_router.get(
    path="",
    response_model=Cpu,
    response_description="Returns all the information of the CPU.",
    status_code=200
)
async def get_cpu(command_manager: Annotated[CommandManager, Security(auth_user)]) -> Cpu:
    """Get the CPU information.

    Args:
        command_manager: To execute commands in the shell.

    Returns:
        The CPU information.

    Raises:
        HTTP Error 500: If there is an error in the command manager.
    """
    try:
        return await CpuManager(command_manager).get_cpu()
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))


@cpu_router.get(
    path="/use",
    response_model=float,
    response_description="Returns the use of CPU.",
    status_code=200
)
async def get_cpu_use(command_manager: Annotated[CommandManager, Security(auth_user)]) -> float:
    """Get the CPU use.

    Args:
        command_manager: To execute commands in the shell.

    Returns:
        The CPU use.

    Raises:
        HTTP Error 500: If there is an error in the command manager.
    """
    try:
        return await CpuManager(command_manager).get_cpu_use()
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))


@cpu_router.get(
    path="/temperature",
    response_model=float,
    response_description="Returns the temperature of the CPU.",
    status_code=200
)
async def get_cpu_temperature(command_manager: Annotated[CommandManager, Security(auth_user)]) -> float:
    """Get the CPU temperature.

    Args:
        command_manager: To execute commands in the shell.

    Returns:
        The CPU temperature.

    Raises:
        HTTP Error 500: If there is an error in the command manager.
    """
    try:
        return await CpuManager(command_manager).get_cpu_temperature()
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))
