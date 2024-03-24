"""This module contains the crontab endpoint for the API REST."""
from typing import Annotated

from crontab_lib import CronJob, CrontabManager, NonexistentCrontabFileError, InvalidCronFormatError
from fastapi import APIRouter, Security, HTTPException
from shell_executor_lib import CommandManager, CommandError

from api.dependencies import auth_user

crontab_router = APIRouter(
    prefix="/crontab",
    tags=["Crontab"],
)


@crontab_router.get(
    path="/",
    response_model=list[CronJob],
    response_description="Returns a list of cron jobs.",
    status_code=200
)
async def get_crontabs(command_manager: Annotated[CommandManager, Security(auth_user)]) -> list[CronJob]:
    """Get the cron jobs from the crontab file.

    Args:
        command_manager: To make commands in the shell.

    Returns:
        The cron jobs from the crontab file.
    """
    try:
        return await CrontabManager(command_manager).get_cron_jobs()
    except NonexistentCrontabFileError as nonexistent_crontab_file_error:
        raise HTTPException(status_code=404, detail=str(nonexistent_crontab_file_error))
    except CommandError as command_error:
        raise HTTPException(status_code=500, detail=str(command_error))


@crontab_router.post(
    path="/",
    response_model=CronJob,
    response_description="Return the new cron job.",
    status_code=201
)
async def add_crontab(
    cron_job: CronJob,
    command_manager: Annotated[CommandManager, Security(auth_user)]
) -> CronJob:
    """Add a cron job in the crontab file.

    Args:
        cron_job: The cron job to be added.
        command_manager: To make commands in the shell.

    Returns:
        The new cron job.
    """
    try:
        await CrontabManager(command_manager).add_cron_job(cron_job)
        return cron_job
    except InvalidCronFormatError as invalid_cron_format_error:
        raise HTTPException(status_code=400, detail=str(invalid_cron_format_error))
    except CommandError as command_error:
        raise HTTPException(status_code=500, detail=str(command_error))


@crontab_router.put(
    path="/",
    response_model=CronJob,
    response_description="Return the updated cron job.",
    status_code=200
)
async def update_crontab(
    old_cron_job: CronJob,
    new_cron_job: CronJob,
    command_manager: Annotated[CommandManager, Security(auth_user)]
) -> CronJob:
    """Edit a cron job in the crontab file.

    Args:
        old_cron_job: The old cron job to be removed.
        new_cron_job: The new cron job to be added.
        command_manager: To make commands in the shell.

    Returns:
        The updated cron job.
    """
    try:
        await CrontabManager(command_manager).edit_cron_job(new_cron_job, old_cron_job)
        return new_cron_job
    except InvalidCronFormatError as invalid_cron_format_error:
        raise HTTPException(status_code=400, detail=str(invalid_cron_format_error))
    except NonexistentCrontabFileError as nonexistent_crontab_file_error:
        raise HTTPException(status_code=404, detail=str(nonexistent_crontab_file_error))
    except CommandError as command_error:
        raise HTTPException(status_code=500, detail=str(command_error))


@crontab_router.delete(
    path="/",
    response_description="Delete the cron job.",
    status_code=204
)
async def delete_crontab(
    cron_job: CronJob,
    command_manager: Annotated[CommandManager, Security(auth_user)]
) -> None:
    """Delete a cron job from the crontab file.

    Args:
        cron_job: The cron job to be deleted.
        command_manager: To make commands in the shell.
    """
    try:
        await CrontabManager(command_manager).delete_cron_job(cron_job)
    except NonexistentCrontabFileError as nonexistent_crontab_file_error:
        raise HTTPException(status_code=404, detail=str(nonexistent_crontab_file_error))
    except CommandError as command_error:
        raise HTTPException(status_code=500, detail=str(command_error))
