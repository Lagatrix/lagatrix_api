"""This module contains the user endpoint for the API REST."""
from typing import Annotated

from fastapi import HTTPException, APIRouter
from fastapi.params import Security
from groups_users_lib import GroupNotExistError, UserNotExistError, Group, \
    GroupManager, GroupExistError
from shell_executor_lib import CommandError, PrivilegesError, CommandManager
from starlette import status

from api.dependencies import auth_user

group_router = APIRouter(
    prefix="/group",
    tags=["Groups"],
)


@group_router.get(
    path="/",
    response_model=list[Group],
    response_description="Returns a list of groups.",
    status_code=200
)
async def get_groups(command_manager: Annotated[CommandManager, Security(auth_user)]) -> list[Group]:
    """Get the list of groups.

    Args:
        command_manager: The command manager to execute commands.

    Returns:
        The list of groups.
    """
    try:
        return await GroupManager(command_manager).get_groups()
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))


@group_router.get(
    path="/{group}",
    response_model=Group,
    response_description="Returns a group.",
    status_code=200
)
async def get_group(command_manager: Annotated[CommandManager, Security(auth_user)], group: str) -> Group:
    """Get a group.

    Args:
        group: The name of group to get.
        command_manager: The command manager to execute commands.

    Returns:
        The group.

    Raises:
        HTTP Error 400: If you don't send the group.
        HTTP Error 404: If the group not exist.
    """
    group_manager: GroupManager = GroupManager(command_manager)

    if group is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The group is required.")

    try:
        return await group_manager.get_group(group)
    except GroupNotExistError as group_not_exist_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(group_not_exist_error))
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))


@group_router.post(
    path="/",
    response_model=Group,
    response_description="Returns the added group.",
    status_code=201
)
async def post_group(
    group: Group,
    command_manager: Annotated[CommandManager, Security(auth_user)]
) -> Group:
    """Create a group.

    Args:
        group: The group to create.
        command_manager: The command manager to execute commands.

    Raises:
        HTTP Error 400: If you don't send the group.
        HTTP Error 403: If you don't have privileges to execute the command.
        HTTP Error 409: If the group already exist.
        HTTP Error 500: If there is an error in the command manager.
    """
    group_manager: GroupManager = GroupManager(command_manager)

    if group is None or group.name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The group is required.")

    try:
        await group_manager.add_group(group)
        return await group_manager.get_group(group.name)
    except ValueError as format_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(format_error))
    except PrivilegesError as privileges_error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(privileges_error))
    except UserNotExistError as user_not_exist_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(user_not_exist_error))
    except GroupExistError as group_exist_error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(group_exist_error))
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))


@group_router.put(
    path="/{group_name}",
    response_model=Group,
    response_description="Returns the updated group.",
    status_code=200
)
async def put_group(
    group: Group,
    command_manager: Annotated[CommandManager, Security(auth_user)],
    group_name: str
) -> Group:
    """Update a group.

    Args:
        group: The group to update.
        command_manager: The command manager to execute commands.
        group_name: The name of the group to update.

    Raises:
        HTTP Error 400: If you don't send the group.
        HTTP Error 403: If you don't have privileges to execute the command.
        HTTP Error 404: If the group not exist.
        HTTP Error 500: If there is an error in the command manager.
    """
    group_manager: GroupManager = GroupManager(command_manager)

    if group is None or group.name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The group is required.")

    try:
        await group_manager.edit_group(group_name, group)
        return await group_manager.get_group(group.name)
    except ValueError as format_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(format_error))
    except PrivilegesError as privileges_error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(privileges_error))
    except GroupNotExistError as group_not_exist_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(group_not_exist_error))
    except GroupExistError as group_exist_error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(group_exist_error))
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))


@group_router.post(
    path="/{group_name}/add/{user}",
    response_model=Group,
    response_description="Returns the updated group.",
    status_code=200
)
async def add_user_to_group(
    command_manager: Annotated[CommandManager, Security(auth_user)],
    group_name: str,
    user: str
) -> Group:
    """Add a user to a group.

    Args:
        group_name: The group to add the user.
        user: The user to add to the group.
        command_manager: The command manager to execute commands.

    Raises:
        HTTP Error 400: If you don't send the group.
        HTTP Error 400: If you don't send the user.
        HTTP Error 403: If you don't have privileges to execute the command.
        HTTP Error 404: If the group not exist.
        HTTP Error 404: If the user not exist.
        HTTP Error 500: If there is an error in the command manager.
    """
    group_manager: GroupManager = GroupManager(command_manager)

    if group_name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The group is required.")

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user is required.")

    try:
        await group_manager.add_user_to_group(group_name, user)
        return await group_manager.get_group(group_name)
    except PrivilegesError as privileges_error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(privileges_error))
    except GroupNotExistError as group_not_exist_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(group_not_exist_error))
    except UserNotExistError as user_not_exist_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(user_not_exist_error))
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))


@group_router.delete(
    path="/{group_name}/remove/{user}",
    response_model=Group,
    response_description="Returns the updated group.",
    status_code=200
)
async def remove_user_from_group(
    command_manager: Annotated[CommandManager, Security(auth_user)],
    group_name: str,
    user: str
) -> Group:
    """Remove a user from a group.

    Args:
        group_name: The group to remove the user.
        user: The user to remove from the group.
        command_manager: The command manager to execute commands.

    Raises:
        HTTP Error 400: If you don't send the group.
        HTTP Error 400: If you don't send the user.
        HTTP Error 403: If you don't have privileges to execute the command.
        HTTP Error 404: If the group not exist.
        HTTP Error 404: If the user not exist.
        HTTP Error 500: If there is an error in the command manager.
    """
    group_manager: GroupManager = GroupManager(command_manager)

    if group_name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The group is required.")

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user is required.")

    try:
        await group_manager.remove_user_from_group(group_name, user)
        return await group_manager.get_group(group_name)
    except PrivilegesError as privileges_error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(privileges_error))
    except GroupNotExistError as group_not_exist_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(group_not_exist_error))
    except UserNotExistError as user_not_exist_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(user_not_exist_error))
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))


@group_router.delete(
    path="/{group_name}",
    response_model=None,
    status_code=200
)
async def delete_group(
    command_manager: Annotated[CommandManager, Security(auth_user)],
    group_name: str
) -> None:
    """Delete a group.

    Args:
        group_name: The group to delete.
        command_manager: The command manager to execute commands.

    Raises:
        HTTP Error 400: If you don't send the group.
        HTTP Error 403: If you don't have privileges to execute the command.
        HTTP Error 404: If the group not exist.
        HTTP Error 500: If there is an error in the command manager.
    """
    group_manager: GroupManager = GroupManager(command_manager)

    if group_name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The group is required.")

    try:
        await group_manager.delete_group(group_name)
    except PrivilegesError as privileges_error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(privileges_error))
    except GroupNotExistError as group_not_exist_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(group_not_exist_error))
    except CommandError as command_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(command_error))
