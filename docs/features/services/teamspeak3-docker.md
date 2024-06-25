# TeamSpeak 3

## Overview

TeamSpeak3 is the most popular VOIP program for gamers.

But have you considered using Mumble? Not only is it free, but it has features and performance far superior to Teamspeak3.

## Setup

Sticking with TS3? Alright, I tried.

## Configuring Auth

In your auth project's settings file (`aa-docker/conf/local.py`), do the following:

- Add `'allianceauth.services.modules.teamspeak',` to your `INSTALLED_APPS` list
- Append the following to your auth project's settings file:

```python
# Teamspeak3 Configuration
TEAMSPEAK3_SERVER_IP = os.environ.get('TEAMSPEAK3_SERVER_IP', '127.0.0.1')
TEAMSPEAK3_SERVER_PORT = os.environ.get('TEAMSPEAK3_SERVER_PORT', 10011)
TEAMSPEAK3_SERVERQUERY_USER = os.environ.get('TEAMSPEAK3_SERVERQUERY_USER', "serverquery")
TEAMSPEAK3_SERVERQUERY_PASSWORD = os.environ.get('TEAMSPEAK3_SERVERQUERY_PASSWORD', "")
TEAMSPEAK3_VIRTUAL_SERVER = os.environ.get('TEAMSPEAK3_VIRTUAL_SERVER', 1)
TEAMSPEAK3_PUBLIC_URL = SITE_URL

CELERYBEAT_SCHEDULE['run_ts3_group_update'] = {
    'task': 'allianceauth.services.modules.teamspeak3.tasks.run_ts3_group_update',"
    'schedule': crontab(minute='*/30'),
}
```

Add the following lines to your `.env` file

```env
# Temspeak
TEAMSPEAK3_SERVERQUERY_USER = "serverquery"
TEAMSPEAK3_SERVERQUERY_PASSWORD = ""
```

## Docker Installation

Add the following to your `docker-compose.yml` under the `services:` section

```docker
  teamspeak:
    image: teamspeak:3.13
    restart: always
    environment:
      TS3SERVER_LICENSE: accept
    ports:
      - 9987:9987/udp
      - 30033:30033
    volumes:
      - teamspeak-data:/var/ts3server/
    logging:
      driver: "json-file"
      options:
        max-size: "10Mb"
        max-file: "5"
```

### Update Settings

In (`aa-docker/conf/local.py`), update the following

- `TEAMSPEAK_VIRTUAL_SERVER` is the virtual server ID of the server to be managed - it will only ever not be 1 if your server is hosted by a professional company
- `TEAMSPEAK3_PUBLIC_URL` is the public address of your TeamSpeak server. Do not include any leading http:// or teamspeak://

In your `.env` file, update the following, obtained from the logs of the Teamspeak server initaliztion `docker compose logs teamspeak`

- `TEAMSPEAK3_SERVERQUERY_USER` is `loginname` from the above bash command (usually `serveradmin`)
- `TEAMSPEAK3_SERVERQUERY_PASSWORD` is `password` following the equals in `serveradmin_password=`

Once settings are entered, run migrations and restart your stack

```shell
docker compose --env-file=.env up -d
docker compose exec allianceauth_gunicorn bash
auth migrate
```

### Generate User Account

And now we can generate ourselves a user account. Navigate to the services in Alliance Auth for your user account and press the checkmark for TeamSpeak 3.

Click the URL provided to automatically connect to our server. It will prompt you to redeem the serveradmin token, enter the `token` from startup.

### Groups

Now we need to make groups. AllianceAuth handles groups in teamspeak differently: instead of creating groups it creates an association between groups in TeamSpeak and groups in AllianceAuth. Go ahead and make the groups you want to associate with auth groups, keeping in mind multiple TeamSpeak groups can be associated with a single auth group.

Navigate back to the AllianceAuth admin interface (example.com/admin) and under `Teamspeak3`, select `Auth / TS Groups`.

In the top-right corner click, first click on `Update TS3 Groups` to fetch the newly created server groups from TS3 (this may take a minute to complete). Then click on `Add Auth / TS Group` to link Auth groups with TS3 server groups.

The dropdown box provides all auth groups. Select one and assign TeamSpeak groups from the panels below. If these panels are empty, wait a minute for the database update to run, or see the [troubleshooting section](#ts-group-models-not-populating-on-admin-site) below.

## Troubleshooting

### `Insufficient client permissions (failed on Invalid permission: 0x26)`

Using the advanced permissions editor, ensure the `Guest` group has the permission `Use Privilege Keys to gain permissions` (under `Virtual Server` expand the `Administration` section)

To enable advanced permissions, on your client go to the `Tools` menu, `Application`, and under the `Misc` section, tick `Advanced permission system`

### TS group models not populating on admin site

The method which populates these runs every 30 minutes. To populate manually you start the process from the admin site or from the Django shell.

#### Admin Site

Navigate to the AllianceAuth admin interface and under `Teamspeak3`, select `Auth / TS Groups`.

Then, in the top-right corner click, click on `Update TS3 Groups` to start the process of fetching the server groups from TS3 (this may take a minute to complete).

#### Django Shell

Start a django shell with:

```shell
docker compose exec allianceauth_gunicorn bash
auth shell
```

And execute the update as follows:

```python
from allianceauth.services.modules.teamspeak3.tasks import Teamspeak3Tasks
Teamspeak3Tasks.run_ts3_group_update()
```

Ensure that command does not return an error.

### `2564 access to default group is forbidden`

This usually occurs because auth is trying to remove a user from the `Guest` group (group ID 8). The guest group is only assigned to a user when they have no other groups, unless you have changed the default teamspeak server config.

Teamspeak servers v3.0.13 and up are especially susceptible to this. Ensure the Channel Admin Group is not set to `Guest (8)`. Check by right clicking on the server name, `Edit virtual server`, and in the middle of the panel select the `Misc` tab.

### `TypeError: string indices must be integers, not str`

This error generally means teamspeak returned an error message that went unhandled. The full traceback is required for proper debugging, which the logs do not record. Please check the superuser notifications for this record and get in touch with a developer.

### `3331 flood ban`

This most commonly happens when your teamspeak server is externally hosted. You need to add the auth server IP to the teamspeak serverquery whitelist. This varies by provider.

If you have SSH access to the server hosting it, you need to locate the teamspeak server folder and add the auth server IP on a new line in  `query_ip_allowlist.txt` (named `query_ip_whitelist.txt` on older teamspeak versions).

### `520 invalid loginname or password`

The serverquery account login specified in local.py is incorrect. Please verify `TEAMSPEAK3_SERVERQUERY_USER` and `TEAMSPEAK3_SERVERQUERY_PASSWORD`. The [installation section](#update-settings) describes where to get them.

### `2568 insufficient client permissions`

This usually occurs if you've created a separate serverquery user to use with auth. It has not been assigned sufficient permissions to complete all the tasks required of it. The full list of required permissions is not known, so assign liberally.

## Permissions

To use and configure this service, users will require some of the following.

```{eval-rst}
+---------------------------------------+------------------+--------------------------------------------------------------------------+
| Permission                            | Admin Site       | Auth Site                                                                |
+=======================================+==================+==========================================================================+
| teamspeak.access_teamspeak            | None             | Can Access the TeamSpeak Service                                         |
+---------------------------------------+------------------+--------------------------------------------------------------------------+
| teamspeak.add_authts                  | Can Add Model    | None                                                                     |
+---------------------------------------+------------------+--------------------------------------------------------------------------+
| teamspeak.change_authts               | Can Change Model | None                                                                     |
+---------------------------------------+------------------+--------------------------------------------------------------------------+
| teamspeak.delete_authts               | Can Delete Model | None                                                                     |
+---------------------------------------+------------------+--------------------------------------------------------------------------+
| teamspeak.view_authts                 | Can View Model   | None                                                                     |
+---------------------------------------+------------------+--------------------------------------------------------------------------+
```
