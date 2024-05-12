"""This module contains the user endpoint for the API REST."""
from typing import Annotated

from fastapi import HTTPException, APIRouter
from fastapi.params import Security
from groups_users_lib import User, UserManager, GroupNotExistError, UserExistError, UserNotExistError, UserInUseError
from shell_executor_lib import CommandError, PrivilegesError, CommandManager
from starlette import status

from api.dependencies import auth_user

user_router = APIRouter(
    prefix="/user",
    tags=["Users"],
)


@user_router.get(
    path="/login",
    response_model=str,
    status_code=200
)
async def make_login(command_manager: Annotated[CommandManager, Security(auth_user)]) -> str:
    """Make login.

    Args:
        command_manager: The command manager to execute commands.

    Returns:
        The welcome message.
    """
    return f'Welcome {command_manager.user}!'


@user_router.get(
    path="/",
    response_model=list[User],
    response_description="Returns a list of users.",
    status_code=200
)
async def get_users(command_manager: Annotated[CommandManager, Security(auth_user)]) -> list[User]:
    """Get the list of users.

    Args:
        command_manager: The command manager to execute commands.

    Returns:
        The list of users.

    Raises:
        HTTP Error 500: If there is an error in the command manager.
    """
    try:
        return await UserManager(command_manager).get_users()
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))


@user_router.get(
    path="/{user}",
    response_model=User,
    response_description="Returns a user.",
    status_code=200
)
async def get_user(
    user: str,
    command_manager: Annotated[CommandManager, Security(auth_user)]
) -> User:
    """Get a user.

    Args:
        user: The name of user to get.
        command_manager: The command manager to execute commands.

    Returns:
        The user.

    Raises:
        HTTP Error 400: If you don't send the user.
        HTTP Error 404: If the user not exist.
        HTTP Error 500: If there is an error in the command manager.
    """
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user is required.")

    try:
        return await UserManager(command_manager).get_user(user)
    except UserNotExistError as user_not_exist_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(user_not_exist_error))
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))


@user_router.post(
    path="/",
    response_model=User,
    response_description="Returns the added user.",
    status_code=201
)
async def post_user(
    user: User,
    command_manager: Annotated[CommandManager, Security(auth_user)]
) -> User:
    """Create a user.

    Args:
        user: The user to create.
        command_manager: The command manager to execute commands.

    Raises:
        HTTP Error 400: If you don't send the user.
        HTTP Error 400: If the group not exist.
        HTTP Error 403: If you don't have privileges to execute the command.
        HTTP Error 409: If the user already exist.
        HTTP Error 500: If there is an error in the command manager.
    """
    user_manager: UserManager = UserManager(command_manager)

    if user is None or user.name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user is required.")

    try:
        await user_manager.add_user(user)
        return await user_manager.get_user(user.name)
    except ValueError as formats_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(formats_error))
    except PrivilegesError as privileges_error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(privileges_error))
    except GroupNotExistError as group_not_exist_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(group_not_exist_error))
    except UserExistError as user_exist_error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(user_exist_error))
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))


@user_router.put(
    path="/{user}",
    response_model=User,
    response_description="Returns the updated user.",
    status_code=200
)
async def put_user(
    user: str,
    user_changes: User,
    command_manager: Annotated[CommandManager, Security(auth_user)]
) -> User:
    """Update a user.

    Args:
        user: The user to update.
        user_changes: The user with the new data.
        command_manager: The command manager to execute commands.

    Raises:
        HTTP Error 400: If you don't send the user.
        HTTP Error 400: If you don't send the user_.
        HTTP Error 400: If the group not exist.
        HTTP Error 403: If you don't have privileges to execute the command.
        HTTP Error 404: If the user not exist.
        HTTP Error 500: If there is an error in the command manager.
    """
    user_manager: UserManager = UserManager(command_manager)

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The username is required.")

    if user_changes is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user changes is required.")

    try:
        await user_manager.edit_user(user, user_changes, user_changes.password)
        return await user_manager.get_user(user_changes.name if user_changes.name else user)
    except (ValueError, GroupNotExistError) as formats_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(formats_error))
    except PrivilegesError as privileges_error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(privileges_error))
    except UserNotExistError as user_not_exist_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(user_not_exist_error))
    except UserExistError as user_exist_error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(user_exist_error))
    except UserInUseError as user_in_use_error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(user_in_use_error))
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))


@user_router.delete(
    path="/{user}",
    status_code=204,
)
async def delete_user(
    user: str,
    command_manager: Annotated[CommandManager, Security(auth_user)]
) -> None:
    """Delete a user.

    Args:
        user: The user to delete.
        command_manager: The command manager to execute commands.

    Raises:
        HTTP Error 400: If you don't send the user.
        HTTP Error 403: If you don't have privileges to execute the command.
        HTTP Error 404: If the user not exist.
        HTTP Error 500: If there is an error in the command manager.
    """
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The username is required.")

    try:
        await UserManager(command_manager).delete_user(user)
    except UserNotExistError as user_not_exist_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(user_not_exist_error))
    except PrivilegesError as privileges_error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(privileges_error))
    except UserInUseError as user_in_use_error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(user_in_use_error))
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))
