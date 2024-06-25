# Migrating your Docker Compose stack from AA V3.x to AA v4.x

Our Docker Compose stack has both changed significantly, and simplified itself drastically depending on your level of familiarity with Docker.

We have Removed our need to run Supervisor inside the container to run the various tasks needed, and split the stack into multiple containers responsible for each task, as well as modernized many elements.

## aa-docker/conf/*

We are bundling a few often customized files along side our AA install for easier modification by users, you will need to download these into aa-docker/conf

```shell
wget https://gitlab.com/allianceauth/allianceauth/-/raw/v4.x/docker/conf/celery.py
wget https://gitlab.com/allianceauth/allianceauth/-/raw/v4.x/docker/conf/urls.py
wget https://gitlab.com/allianceauth/allianceauth/-/raw/v4.x/docker/conf/memory_check.sh
wget https://gitlab.com/allianceauth/allianceauth/-/raw/v4.x/docker/conf/redis_healthcheck.sh
```

## Docker Compose

At this point you should take a copy of your docker-compose and take note of any additional volumes or configurations you have, and why.

Take a complete backup of your local.py, docker-compose and SQL database.

`docker compose down`

Replace your conf/nginx.conf with the contents of <https://gitlab.com/allianceauth/allianceauth/-/raw/v4.x/docker/conf/nginx.conf>

Replace your docker-compose.yml with the contents of <https://gitlab.com/allianceauth/allianceauth/-/raw/v4.x/docker/docker-compose.yml>

V3.x installs likely used a dedicated database for Nginx Proxy Manager, you can either setup NPM again without a database, or uncomment the sections noted to maintain this configuration

```docker-compose
  proxy:
  ...
    # Uncomment this section to use a dedicated database for Nginx Proxy Manager
    environment:
      DB_MYSQL_HOST: "proxy-db"
      DB_MYSQL_PORT: 3306
      DB_MYSQL_USER: "npm"
      DB_MYSQL_PASSWORD: "${PROXY_MYSQL_PASS?err}"
      DB_MYSQL_NAME: "npm"
  ...
  # Uncomment this section to use a dedicated database for Nginx Proxy Manager
  proxy-db:
    image: 'jc21/mariadb-aria:latest'
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: "${PROXY_MYSQL_PASS_ROOT?err}"
      MYSQL_DATABASE: 'npm'
      MYSQL_USER: 'npm'
      MYSQL_PASSWORD: "${PROXY_MYSQL_PASS?err}"
    ports:
      - 3306
    volumes:
      - proxy-db:/var/lib/mysql
    logging:
      driver: "json-file"
      options:
        max-size: "1Mb"
        max-file: "5"
```

## .env

You will need to add some entries to your .env file

```env
AA_DB_CHARSET=utf8mb4
GF_SECURITY_ADMIN_USERNAME=admin
```

and
`GF_SECURITY_ADMIN_PASSWORD`

The password field is intentionally not filled so that you create one. You can either use the grafana credentials you have been using, or create a suitably secure password now.

You will also need to update the `AA_DOCKER_TAG` to the version of V4.x you want to install. Either follow the pattern or check <https://gitlab.com/allianceauth/allianceauth/-/releases>

## (Optional) Build Custom Container

If you are using a docker container with a requirements.txt, You will need to reinstate some customizations.

Modify `docker-compose.yml`, as follows.

* Comment out the `image` line under `allianceauth`
* Uncomment the `build` section
* e.g.

  ```docker
    x-allianceauth-base: &allianceauth-base
    # image: ${AA_DOCKER_TAG?err}
    build:
      context: .
      dockerfile: custom.dockerfile
      args:
        AA_DOCKER_TAG: ${AA_DOCKER_TAG?err}
    restart: always
  ...
  ```

Now build your custom image

```shell
docker compose pull
docker compose build
```

## Bring docker back up, migrate, collect static

```shell
docker compose --env-file=.env up -d --remove-orphans

docker compose exec allianceauth_gunicorn bash

allianceauth update myauth
auth migrate
auth collectstatic --clear
```
