# Openfire

An alternate install guide for Openfire using Docker, better suited to an Alliance Auth Docker install

Openfire is a Jabber (XMPP) server.

## Configuring Auth

In your auth project's settings file (`aa-docker/conf/local.py`), do the following:

- Add `'allianceauth.services.modules.openfire',` to your `INSTALLED_APPS` list
- Append the following to your auth project's settings file:

```python
# Jabber Configuration
JABBER_URL = SITE_URL
JABBER_PORT = os.environ.get('JABBER_PORT', 5223)
JABBER_SERVER = SITE_URL
OPENFIRE_ADDRESS = SITE_URL
OPENFIRE_SECRET_KEY = os.environ.get('OPENFIRE_SECRET_KEY', '')
BROADCAST_USER = ""
BROADCAST_USER_PASSWORD = os.environ.get('BROADCAST_USER_PASSWORD', '127.0.0.1')
BROADCAST_SERVICE_NAME = "broadcast"
```

Add the following lines to your `.env` file

```env
# Openfire
OPENFIRE_SECRET_KEY = superuser_password
BROADCAST_USER_PASSWORD = icesecretwrite

```

Finally, restart your stack and run migrations

```shell
docker compose --env-file=.env up -d
docker compose exec allianceauth_gunicorn bash
auth migrate
```

## Docker Installation

Add the following to your `docker-compose.yml` under the `services:` section

```docker
  openfire:
    image: nasqueron/openfire:4.7.5
    ports:
      - "5222:5222/tcp"
      - "5223:5223/tcp"
      - "7777:7777/tcp"
    volumes:
      - openfire-data:/var/lib/openfire
    depends_on:
    - auth_mysql
  logging:
    driver: "json-file"
    options:
      max-size: "50Mb"
      max-file: "5"
```

### Create Database

We have a Mariadb container already as part of the Alliance Auth stack, enter it and create a database for it.

```shell
docker exec -it auth_mysql
mysql -u root -p $AA_DB_ROOT_PASSWORD
```

```sql
create database alliance_jabber;
grant all privileges on alliance_jabber . * to 'aauth'@'localhost';
exit;
exit
```

### Configure Webserver

In Nginx Proxy Manager `http://yourdomain:81/`, go to `Proxy Hosts`, Click `Add Proxy Host`. You can refer to :doc:`/installation-containerized/docker`

Domain Name: `jabber.yourdomain`
Forward Hostname `openfire`
forward port `9090` for http, `9091` for https

### Web Configuration

The remainder of the setup occurs through Openfire’s web interface. Navigate to <http://jabber.yourdomain.com>

Select your language, our guide will assume English

Under Server Settings, set the Domain to `jabber.yourdomain.com` replacing it with your actual domain. Don’t touch the rest.

Under Database Settings, select `Standard Database Connection`

On the next page, select `MySQL` from the dropdown list and change the following:

- `[server]`: `auth_mysql`
- `[database]`: `alliance_jabber`
- `[user]`: `aauth`
- `[password]`: Your database users password

If Openfire returns with a failed to connect error, re-check these settings. Note the lack of square brackets.

Under Profile Settings, leave `Default` selected.

Create an administrator account. The actual name is irrelevant, just don’t lose this login information.

Finally, log in to the console with your admin account.

Edit your auth project's settings file (`aa-docker/conf/local.py`) and enter the values you just set:

- `JABBER_URL` is the pubic address of your jabber server
- `JABBER_PORT` is the port for clients to connect to (usually 5223)
- `JABBER_SERVER` is the name of the jabber server. If you didn't alter it during install it'll usually be your domain (eg `jabber.example.com`)
- `OPENFIRE_ADDRESS` is the web address of Openfire's web interface. Use http:// with port 9090 or https:// with port 9091 if you configure SSL in Openfire and Nginx Proxy Manager

### REST API Setup

Navigate to the `plugins` tab, and then `Available Plugins` on the left navigation bar. You’ll need to fetch the list of available plugins by clicking the link.

Once loaded, press the green plus on the right for `REST API`.

Navigate the `Server` tab, `Sever Settings` subtab. At the bottom of the left navigation bar select `REST API`.

Select `Enabled`, and `Secret Key Auth`. Update your auth project's settings with this secret key as `OPENFIRE_SECRET_KEY`.

### Broadcast Plugin Setup

Navigate to the `Users/Groups` tab and select `Create New User` from the left navigation bar.

Pick a username (e.g. `broadcast`) and password for your ping user. Enter these in your auth project's settings file as `BROADCAST_USER` and `BROADCAST_USER_PASSWORD`. Note that `BROADCAST_USER` needs to be in the format `user@example.com` matching your jabber server name. Press `Create User` to save this user.

Broadcasting requires a plugin. Navigate to the `plugins` tab, press the green plus for the `Broadcast` plugin.

Navigate to the `Server` tab, `Server Manager` subtab, and select `System Properties`. Enter the following:

- Name: `plugin.broadcast.disableGroupPermissions`
  - Value: `True`
  - Do not encrypt this property value
- Name: `plugin.broadcast.allowedUsers`
  - Value: `broadcast@example.com`, replacing the domain name with yours
  - Do not encrypt this property value

If you have troubles getting broadcasts to work, you can try setting the optional (you will need to add it) `BROADCAST_IGNORE_INVALID_CERT` setting to `True`. This will allow invalid certificates to be used when connecting to the Openfire server to send a broadcast.

### Preparing Auth

Once all settings are entered, run migrations and restart Gunicorn and Celery.

### Group Chat

Channels are available which function like a chat room. Access can be controlled either by password or ACL (not unlike mumble).

Navigate to the `Group Chat` tab and select `Create New Room` from the left navigation bar.

- Room ID is a short, easy-to-type version of the room’s name users will connect to
- Room Name is the full name for the room
- Description is short text describing the room’s purpose
- Set a password if you want password authentication
- Every other setting is optional. Save changes.

Now select your new room. On the left navigation bar, select `Permissions`.

ACL is achieved by assigning groups to each of the three tiers: `Owners`, `Admins` and `Members`. `Outcast` is the blacklist. You’ll usually only be assigning groups to the `Member` category.

## Permissions

To use this service, users will require some of the following.

```{eval-rst}
+---------------------------------------+------------------+--------------------------------------------------------------------------+
| Permission                            | Admin Site       | Auth Site                                                                |
+=======================================+==================+==========================================================================+
| openfire.access_openfire              | None             | Can Access the Openfire Service                                          |
+---------------------------------------+------------------+--------------------------------------------------------------------------+
```
