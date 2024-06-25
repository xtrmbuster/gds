# Mumble

An alternate install guide for Mumble using Docker, better suited to an Alliance Auth Docker install

Mumble is a free voice chat server. While not as flashy as TeamSpeak, it has all the functionality and is easier to customize. And is better. I may be slightly biased.

## Configuring Auth

In your auth project's settings file (`aa-docker/conf/local.py`), do the following:

- Add `'allianceauth.services.modules.mumble',` to your `INSTALLED_APPS` list
- Append the following to your auth project's settings file:

```python
# Mumble Configuration
MUMBLE_URL = "mumble.example.com"
```

Add the following lines to your `.env` file

```env
# Mumble
MUMBLE_SUPERUSER_PASSWORD = superuser_password
MUMBLE_ICESECRETWRITE = icesecretwrite
MUMBLE_SERVERPASSWORD = serverpassword
```

Finally, restart your stack and run migrations

```shell
docker compose --env-file=.env up -d
docker compose exec allianceauth_gunicorn bash
auth migrate
```

## Docker Installations

### Installing Mumble and Authenticator

Inside your `aa-docker` directory, clone the authenticator to a sub directory as follows

```shell
git clone https://gitlab.com/allianceauth/mumble-authenticator.git
```

Add the following to your `docker-compose.yml` under the `services:` section

```docker
  mumble-server:
    image: mumblevoip/mumble-server:latest
    restart: always
    environment:
    - MUMBLE_SUPERUSER_PASSWORD=${MUMBLE_SUPERUSER_PASSWORD}
    - MUMBLE_CONFIG_ice="tcp -h 127.0.0.1 -p 6502"
    - MUMBLE_CONFIG_icesecretwrite=${MUMBLE_ICESECRETWRITE}
    - MUMBLE_CONFIG_serverpassword=${MUMBLE_SERVERPASSWORD}
    - MUMBLE_CONFIG_opusthreshold=0
    - MUMBLE_CONFIG_suggestPushToTalk=true
    - MUMBLE_CONFIG_suggestVersion=1.4.0
    ports:
      - 64738:64738
      - 64738:64738/udp
    logging:
      driver: "json-file"
      options:
        max-size: "10Mb"
        max-file: "5"

  mumble-authenticator:
    build:
      context: .
      dockerfile: ./mumble-authenticator/Dockerfile
    restart: always
    volumes:
      - ./mumble-authenticator/authenticator.py:/authenticator.py
      - ./mumble-authenticator/authenticator.ini.docker:/authenticator.ini
    environment:
    - MUMBLE_SUPERUSER_PASSWORD=${MUMBLE_SUPERUSER_PASSWORD}
    - MUMBLE_CONFIG_ice="tcp -h 127.0.0.1 -p 6502"
    - MUMBLE_CONFIG_icesecretwrite=${MUMBLE_ICESECRETWRITE}
    - MUMBLE_CONFIG_serverpassword=${MUMBLE_SERVERPASSWORD}
    depends_on:
      - mumble-server
      - auth_mysql
    logging:
      driver: "json-file"
      options:
        max-size: "10Mb"
        max-file: "5"
```

## Permissions

To use this service, users will require some of the following.

```{eval-rst}
+---------------------------------------+------------------+--------------------------------------------------------------------------+
| Permission                            | Admin Site       | Auth Site                                                                |
+=======================================+==================+==========================================================================+
| mumble.access_mumble                  | None             | Can Access the Mumble Service                                            |
+---------------------------------------+------------------+--------------------------------------------------------------------------+
```

## ACL configuration

On a freshly installed mumble server only your superuser has the right to configure ACLs and create channels. The credentials for logging in with your superuser are:

- user: `SuperUser`
- password: *what you defined when configuring your mumble server*

## Optimizing a Mumble Server

The needs and available resources will vary between Alliance Auth installations. Consider yours when applying these settings.

### Bandwidth

<https://wiki.mumble.info/wiki/Murmur.ini#bandwidth>
This is likely the most important setting for scaling a Mumble install, The default maximum Bandwidth is 72000bps Per User. Reducing this value will cause your clients to automatically scale back their bandwidth transmitted, while causing a reduction in voice quality. A value thats still high may cause robotic voices or users with bad connections to drop due entirely due to network load.

Please tune this value to your individual needs, the below scale may provide a rough starting point.
72000 - Superior voice quality - Less than 50 users.
54000 - No noticeable reduction in quality - 50+ Users or many channels with active audio.
36000 - Mild reduction in quality - 100+ Users
30000 - Noticeable reduction in quality but not function - 250+ Users

### Forcing Opus

<https://wiki.mumble.info/wiki/Murmur.ini#opusthreshold>
A Mumble server by default, will fall back to the older CELT codec as soon as a single user connects with an old client. This will significantly reduce your audio quality and likely place higher load on your server. We *highly* reccommend setting this to Zero, to force OPUS to be used at all times. Be aware any users with Mumble clients prior to 1.2.4 (From 2013...) Will not hear any audio.

Our default config sets this as follows

```docker
  mumble-authenticator:
    environment:
      `MUMBLE_CONFIG_opusthreshold=0`
```

### AutoBan and Rate Limiting

<https://wiki.mumble.info/wiki/Murmur.ini#autobanAttempts.2C_autobanTimeframe_and_autobanTime>
The AutoBan feature has some sensible settings by default, You may wish to tune these if your users keep locking themselves out by opening two clients by mistake, or if you are receiving unwanted attention

<https://wiki.mumble.info/wiki/Murmur.ini#messagelimit_and_messageburst>
This too, is set to a sensible configuration by default. Take note on upgrading older installs, as this may actually be set too restrictively and will rate-limit your admins accidentally, take note of the configuration in <https://github.com/mumble-voip/mumble/blob/master/scripts/murmur.ini#L156>

```docker
  mumble-authenticator:
    environment:
      MUMBLE_CONFIG_messagelimit=
      MUMBLE_CONFIG_messageburst=
      MUMBLE_CONFIG_autobanAttempts=10
      MUMBLE_CONFIG_autobanTimeframe=120
      MUMBLE_CONFIG_autobanTime=30
      MUMBLE_CONFIG_autobanSuccessfulConnections=false
```

### "Suggest" Options

There is no way to force your users to update their clients or use Push to Talk, but these options will throw an error into their Mumble Client.

<https://wiki.mumble.info/wiki/Murmur.ini#Miscellany>

We suggest using Mumble 1.4.0+ for your server and Clients, you can tune this to the latest Patch version.
If Push to Talk is to your tastes, configure the suggestion as follows

```docker
  mumble-authenticator:
    environment:
      MUMBLE_CONFIG_suggestVersion=s1.4.287
      MUMBLE_CONFIG_suggestPushToTalk=true

```

## General notes

### Server password

With the default Mumble configuration your mumble server is public. Meaning that everyone who has the address can at least connect to it and might also be able join all channels that don't have any permissions set (Depending on your ACL configured for the root channel).

We have changed this behaviour by setting a Server Password by default, to change this password modify `MUMBLE_SERVERPASSWORD` in `.env`.

Restart the container to apply the change.

```shell
docker compose restart mumble-server
```

It is not reccommended to share/use this password, instead use the Mumble Authenticator whenever possible.

As only registered member can join your mumble server. If you still want to allow guests to join you have 2 options.

- Allow the "Guest" state to activate the Mumble service in your Auth instance
- Use [Mumble temporary links](https://github.com/pvyParts/allianceauth-mumble-temp)

### Enabling Avatars in Overlay (V1.0.0+)

Ensure you have an up to date Mumble-Authenticator, this feature was added in V1.0.0

Edit `authenticator.ini` and change (or add for older installs) This code block.

```ini
;If enabled, textures are automatically set as player's EvE avatar for use on overlay.
avatar_enable = True
;Get EvE avatar images from this location. {charid} will be filled in.
ccp_avatar_url = https://images.evetech.net/characters/{charid}/portrait?size=32
```
