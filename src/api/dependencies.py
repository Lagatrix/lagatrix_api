"""This module contains the dependencies for the API REST."""
import base64
from multiprocessing import AuthenticationError
import binascii
from typing import Annotated

from starlette import status

from fastapi import Header, HTTPException
from shell_executor_lib import CommandManager, CommandError


async def auth_user(
    username: Annotated[str | None, Header(convert_underscores=False)] = None,
    password: Annotated[str | None, Header(convert_underscores=False)] = None
) -> CommandManager:
    """Authenticate the user.

    Args:
        username: Name of username.
        password: Password of the user in base 64.

    Returns:
        CommandManager: The command manager to execute commands.

    Raises:
        HTTP Error 400: If the base 64 is not valid.
        HTTP Error 401: If the user is not authenticated.
        HTTP Error 500: If there is an error in the command manager.
    """
    if username is None or password is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Required headers are missing.')

    try:
        return await CommandManager.init(username, base64.b64decode(password).decode('utf-8'))
    except binascii.Error as b64_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(b64_error))
    except AuthenticationError as auth_error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(auth_error))
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))
