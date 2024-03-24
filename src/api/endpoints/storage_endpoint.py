"""This module contains the storage endpoint for the API REST."""
from typing import Annotated

from fastapi import HTTPException, APIRouter
from fastapi.params import Security
from shell_executor_lib import CommandError, CommandManager
from starlette import status
from storage_lib import Disk, DiskManager

from api.dependencies import auth_user

storage_router = APIRouter(
    prefix="/storage",
    tags=["Storage", "Disks", "Partitions"],
)


@storage_router.get(
    path="/disk/",
    response_model=list[Disk],
    response_description="Returns a list of disk.",
    status_code=200
)
async def get_disks(command_manager: Annotated[CommandManager, Security(auth_user)]) -> list[Disk]:
    """Get the list of disks.

    Args:
        command_manager: The command manager to execute commands.

    Returns:
        The list of disks.

    Raises:
        HTTP Error 500: If there is an error in the command manager.
    """
    try:
        return await DiskManager(command_manager).get_disks()
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))
