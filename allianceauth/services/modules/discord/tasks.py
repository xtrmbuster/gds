import logging
from typing import Any

from celery import shared_task, chain
from requests.exceptions import HTTPError

from django.contrib.auth.models import User
from django.db.models.query import QuerySet

from allianceauth.services.tasks import QueueOnce

from . import __title__
from .app_settings import (
    DISCORD_TASKS_MAX_RETRIES, DISCORD_TASKS_RETRY_PAUSE, DISCORD_SYNC_NAMES
)
from .discord_client import DiscordApiBackoff
from .models import DiscordUser
from .utils import LoggerAddTag


logger = LoggerAddTag(logging.getLogger(__name__), __title__)

# task priority of bulk tasks
BULK_TASK_PRIORITY = 6


@shared_task(
    bind=True, name='discord.update_groups', base=QueueOnce, max_retries=None
)
def update_groups(self, user_pk: int, state_name: str = None) -> None:
    """Update roles on Discord for given user according to his current groups

    Params:
    - user_pk: PK of given user
    - state_name: optional state name to be used
    """
    _task_perform_user_action(self, user_pk, 'update_groups', state_name=state_name)


@shared_task(
    bind=True, name='discord.update_nickname', base=QueueOnce, max_retries=None
)
def update_nickname(self, user_pk: int, nickname: str = None) -> None:
    """Set nickname on Discord for given user to his main character name

    Params:
    - user_pk: PK of given user
    - nickname: optional nickname to be used instead of user's main
    """
    _task_perform_user_action(self, user_pk, 'update_nickname', nickname=nickname)


@shared_task(
    bind=True, name='discord.update_username', base=QueueOnce, max_retries=None
)
def update_username(self, user_pk: int) -> None:
    """Update locally stored Discord username from Discord server for given user

    Params:
    - user_pk: PK of given user
    """
    _task_perform_user_action(self, user_pk, 'update_username')


@shared_task(
    bind=True, name='discord.delete_user', base=QueueOnce, max_retries=None
)
def delete_user(self, user_pk: int, notify_user: bool = False) -> None:
    """Delete Discord user

    Params:
    - user_pk: PK of given user
    """
    _task_perform_user_action(self, user_pk, 'delete_user', notify_user=notify_user)


def _task_perform_user_action(self, user_pk: int, method: str, **kwargs) -> None:
    """perform a user related action incl. managing all exceptions"""
    logger.debug("Starting %s for user with pk %s", method, user_pk)
    user = User.objects.get(pk=user_pk)
    # logger.debug("user %s has state %s", user, user.profile.state)
    if DiscordUser.objects.user_has_account(user):
        logger.info("Running %s for user %s", method, user)
        try:
            success = getattr(user.discord, method)(**kwargs)

        except DiscordApiBackoff as bo:
            logger.info(
                "API back off for %s wth user %s due to %r, retrying in %s seconds",
                method,
                user,
                bo,
                bo.retry_after_seconds
            )
            raise self.retry(countdown=bo.retry_after_seconds)

        except AttributeError:
            raise ValueError(f'{method} not a valid method for DiscordUser')

        except (HTTPError, ConnectionError):
            logger.warning(
                '%s failed for user %s, retrying in %d secs',
                method,
                user,
                DISCORD_TASKS_RETRY_PAUSE,
                exc_info=True
            )
            if self.request.retries < DISCORD_TASKS_MAX_RETRIES:
                raise self.retry(countdown=DISCORD_TASKS_RETRY_PAUSE)
            else:
                logger.error(
                    '%s failed for user %s after max retries',
                    method,
                    user,
                    exc_info=True
                )
        except Exception:
            logger.error(
                '%s for user %s failed due to unexpected exception',
                method,
                user,
                exc_info=True
            )

        else:
            if success is None and method != 'delete_user':
                delete_user.delay(user.pk, notify_user=True)

    else:
        logger.debug(
            'User %s does not have a discord account, skipping %s', user, method
        )


@shared_task(name='discord.update_all_groups')
def update_all_groups() -> None:
    """Update roles for all known users with a Discord account."""
    discord_users_qs = DiscordUser.objects.all()
    _bulk_update_groups_for_users(discord_users_qs)


@shared_task(name='discord.update_groups_bulk')
def update_groups_bulk(user_pks: list) -> None:
    """Update roles for list of users with a Discord account in bulk."""
    discord_users_qs = DiscordUser.objects\
        .filter(user__pk__in=user_pks)\
        .select_related()
    _bulk_update_groups_for_users(discord_users_qs)


def _bulk_update_groups_for_users(discord_users_qs: QuerySet) -> None:
    logger.info(
        "Starting to bulk update discord roles for %d users", discord_users_qs.count()
    )
    update_groups_chain = list()
    for discord_user in discord_users_qs:
        update_groups_chain.append(update_groups.si(discord_user.user.pk))

    chain(update_groups_chain).apply_async(priority=BULK_TASK_PRIORITY)


@shared_task(name='discord.update_all_nicknames')
def update_all_nicknames() -> None:
    """Update nicknames for all known users with a Discord account."""
    discord_users_qs = DiscordUser.objects.all()
    _bulk_update_nicknames_for_users(discord_users_qs)


@shared_task(name='discord.update_nicknames_bulk')
def update_nicknames_bulk(user_pks: list) -> None:
    """Update nicknames for list of users with a Discord account in bulk."""
    discord_users_qs = DiscordUser.objects\
        .filter(user__pk__in=user_pks)\
        .select_related()
    _bulk_update_nicknames_for_users(discord_users_qs)


def _bulk_update_nicknames_for_users(discord_users_qs: QuerySet) -> None:
    logger.info(
        "Starting to bulk update discord nicknames for %d users",
        discord_users_qs.count()
    )
    update_nicknames_chain = list()
    for discord_user in discord_users_qs:
        update_nicknames_chain.append(update_nickname.si(discord_user.user.pk))

    chain(update_nicknames_chain).apply_async(priority=BULK_TASK_PRIORITY)


def _task_perform_users_action(self, method: str, **kwargs) -> Any:
    """Perform an action that concerns a group of users or the whole server
    and that hits the API
    """
    result = None
    try:
        result = getattr(DiscordUser.objects, method)(**kwargs)

    except AttributeError:
        raise ValueError(f'{method} not a valid method for DiscordUser.objects')

    except DiscordApiBackoff as bo:
        logger.info(
            "API back off for %s due to %r, retrying in %s seconds",
            method,
            bo,
            bo.retry_after_seconds
        )
        raise self.retry(countdown=bo.retry_after_seconds)

    except (HTTPError, ConnectionError):
        logger.warning(
            '%s failed, retrying in %d secs',
            method,
            DISCORD_TASKS_RETRY_PAUSE,
            exc_info=True
        )
        if self.request.retries < DISCORD_TASKS_MAX_RETRIES:
            raise self.retry(countdown=DISCORD_TASKS_RETRY_PAUSE)
        else:
            logger.error('%s failed after max retries', method, exc_info=True)

    except Exception:
        logger.error('%s failed due to unexpected exception', method, exc_info=True)

    return result


@shared_task(
    bind=True, name='discord.update_servername', base=QueueOnce, max_retries=None
)
def update_servername(self) -> None:
    """Updates the Discord server name"""
    _task_perform_users_action(self, method="server_name", use_cache=False)


@shared_task(name='discord.update_all_usernames')
def update_all_usernames() -> None:
    """Update all usernames for all known users with a Discord account.
    Also updates the server name
    """
    update_servername.delay()
    discord_users_qs = DiscordUser.objects.all()
    _bulk_update_usernames_for_users(discord_users_qs)


@shared_task(name='discord.update_usernames_bulk')
def update_usernames_bulk(user_pks: list) -> None:
    """Update usernames for list of users with a Discord account in bulk."""
    discord_users_qs = DiscordUser.objects\
        .filter(user__pk__in=user_pks)\
        .select_related()
    _bulk_update_usernames_for_users(discord_users_qs)


def _bulk_update_usernames_for_users(discord_users_qs: QuerySet) -> None:
    logger.info(
        "Starting to bulk update discord usernames for %d users",
        discord_users_qs.count()
    )
    update_usernames_chain = list()
    for discord_user in discord_users_qs:
        update_usernames_chain.append(update_username.si(discord_user.user.pk))

    chain(update_usernames_chain).apply_async(priority=BULK_TASK_PRIORITY)


@shared_task(name='discord.update_all')
def update_all() -> None:
    """Updates groups and nicknames (when activated) for all users."""
    discord_users_qs = DiscordUser.objects.all()
    logger.info(
        'Starting to bulk update all for %s Discord users', discord_users_qs.count()
    )
    update_all_chain = list()
    for discord_user in discord_users_qs:
        update_all_chain.append(update_groups.si(discord_user.user.pk))
        update_all_chain.append(update_username.si(discord_user.user.pk))
        if DISCORD_SYNC_NAMES:
            update_all_chain.append(update_nickname.si(discord_user.user.pk))

    chain(update_all_chain).apply_async(priority=BULK_TASK_PRIORITY)
