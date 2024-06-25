"""Settings for the Discord client.

To overwrite a default set the variable in your local Django settings, e.g:

.. code:: python

    DISCORD_GUILD_NAME_CACHE_MAX_AGE = 7200
"""

from ..utils import clean_setting


DISCORD_API_BASE_URL = clean_setting(
    'DISCORD_API_BASE_URL', 'https://discord.com/api/'
)
"""Base URL for all API calls. Must end with /."""

DISCORD_API_TIMEOUT_CONNECT = clean_setting(
    'DISCORD_API_TIMEOUT', 5
)
"""Low level connect timeout for requests to the Discord API in seconds."""

DISCORD_API_TIMEOUT_READ = clean_setting(
    'DISCORD_API_TIMEOUT', 30
)
"""Low level read timeout for requests to the Discord API in seconds."""

DISCORD_OAUTH_BASE_URL = clean_setting(
    'DISCORD_OAUTH_BASE_URL', 'https://discord.com/api/oauth2/authorize'
)
"""Base authorization URL for Discord Oauth."""

DISCORD_OAUTH_TOKEN_URL = clean_setting(
    'DISCORD_OAUTH_TOKEN_URL', 'https://discord.com/api/oauth2/token'
)
"""Base authorization URL for Discord Oauth."""

DISCORD_GUILD_NAME_CACHE_MAX_AGE = clean_setting(
    'DISCORD_GUILD_NAME_CACHE_MAX_AGE', 3600 * 24
)
"""How long the Discord guild names retrieved from the server
are caches locally in seconds.
"""

DISCORD_ROLES_CACHE_MAX_AGE = clean_setting(
    'DISCORD_ROLES_CACHE_MAX_AGE', 3600 * 1
)
"""How long Discord roles retrieved from the server are caches locally in seconds."""

DISCORD_DISABLE_ROLE_CREATION = clean_setting(
    'DISCORD_DISABLE_ROLE_CREATION', False
)
"""Turns off creation of new roles. In case the rate limit for creating roles is
exhausted, this setting allows the Discord service to continue to function
and wait out the reset. Rate limit is about 250 per 48 hrs.
"""
