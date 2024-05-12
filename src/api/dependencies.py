"""This module contains the dependencies for the API REST."""
import base64
import binascii
from typing import Annotated

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

from fastapi import Header, HTTPException, Depends
from shell_executor_lib import CommandManager, CommandError, AuthenticationError

security = HTTPBasic()


async def auth_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
) -> CommandManager:
    """Authenticate the user.

    Args:
        credentials: The credentials of the user.

    Returns:
        CommandManager: The command manager to execute commands.

    Raises:
        HTTP Error 401: If the user is not authenticated.
        HTTP Error 500: If there is an error in the command manager.
    """
    if credentials.username is None or credentials.password is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str("Invalid credentials"))

    try:
        return await CommandManager.init(credentials.username, credentials.password)
    except AuthenticationError as auth_error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(auth_error))
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))
