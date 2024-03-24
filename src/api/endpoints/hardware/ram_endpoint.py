"""This module contains the RAM endpoint for the API REST."""
from typing import Annotated

from fastapi import APIRouter, Security, HTTPException
from ram_lib import RamManager, RamModule
from shell_executor_lib import CommandManager, CommandError, PrivilegesError
from starlette import status

from api.dependencies import auth_user

ram_router = APIRouter(
    prefix="/ram",
    tags=["RAM"],
)


@ram_router.get(
    path="/",
    response_model=list[RamModule],
    response_description="Returns the RAM information.",
    status_code=200
)
async def get_ram(command_manager: Annotated[CommandManager, Security(auth_user)]) -> list[RamModule]:
    """Get the RAM information.

    Args:
        command_manager: To execute commands in the shell.

    Returns:
        The RAM information.

    Raises:
        HTTP Error 403: If the user does not have the necessary privileges.
        HTTP Error 500: If there is an error in the command manager.
    """
    try:
        return await RamManager(command_manager).get_ram()
    except PrivilegesError as privileges_error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(privileges_error))
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))


@ram_router.get(
    path="/use",
    response_model=dict[str, int],
    response_description="Returns the size and use of RAM.",
    status_code=200
)
async def get_ram_use(command_manager: Annotated[CommandManager, Security(auth_user)]) -> dict[str, int]:
    """Get the RAM size and use.

    Args:
        command_manager: To execute commands in the shell.

    Returns:
        The RAM size and use.

    Raises:
        HTTP Error 500: If there is an error in the command manager.
    """
    try:
        tuple_ram = await RamManager(command_manager).get_use()
        return {"size": tuple_ram[0], "use": tuple_ram[1]}
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))
