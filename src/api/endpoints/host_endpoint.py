"""This module contains the host endpoint for the API REST."""
from typing import Annotated

from fastapi import HTTPException, APIRouter
from fastapi.params import Security
from host_lib import Host, HostManager
from shell_executor_lib import CommandError, CommandManager
from starlette import status

from api.dependencies import auth_user

host_router = APIRouter(
    prefix="/host",
    tags=["Host"],
)


@host_router.get(
    path="",
    response_model=Host,
    response_description="Returns host information.",
    status_code=200
)
async def get_host(command_manager: Annotated[CommandManager, Security(auth_user)]) -> Host:
    """Get the host information.

    Args:
        command_manager: The command manager to execute commands.

    Returns:
        The host information.

    Raises:
        HTTP Error 500: If there is an error in the command manager.
    """
    try:
        return await HostManager(command_manager).get_host()
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))
