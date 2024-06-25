# Web Tuning

## Gunicorn

### Number of workers

The default installation will have 3 workers configured for Gunicorn. This will be fine on most systems, but if your system as more than one core than you might want to increase the number of workers to get better response times. Note that more workers will also need more RAM though.

The number you set this to will depend on your own server environment, how many visitors you have etc. Gunicorn suggests `(2 x $num_cores) + 1` for the number of workers. So for example, if you have 2 cores, you want 2 x 2 + 1 = 5 workers. See [here](https://docs.gunicorn.org/en/stable/design.html#how-many-workers) for the official discussion on this topic.

::::{tabs}
:::{group-tab} Ubuntu 2204, 2404
To have 5 workers change the setting `--workers=x` to `--workers=5` in your `supervisor.conf` file and then reload the supervisor with the following command to activate the change

```shell
systemctl restart supervisor
```

:::
:::{group-tab} CentOS / RHEL
To have 5 workers change the setting `--workers=x` to `--workers=5` in your `supervisor.conf` file and then reload the supervisor with the following command to activate the change

```shell
systemctl restart supervisor
```

:::
:::{group-tab} Docker Compose
To have 5 workers change the setting `--workers=3` to `--workers=5` in your `docker-compose.yml` file and then restart the container as follows

```shell
docker compose up -d
```

:::
::::

## nginx

### nginx repo

We can use the Nginx repositories for a slightly more cutting edge version of Nginx, with more features. Install it to enable the below features

::::{tabs}
:::{group-tab} Ubuntu 2204, 2404
<https://nginx.org/en/linux_packages.html#Ubuntu>
:::
:::{group-tab} CentOS / RHEL
<https://nginx.org/en/linux_packages.html#RHEL>
:::
:::{group-tab} Docker
No package necessary, simply increase `docker compose pull` and `docker compose up -d` to update.
:::
::::

### Brotli Compression

Brotli is a modern compression algorithm designed for the web. Use this with Pre-Compression and E2E Cloudflare compression for best results.

::::{tabs}
:::{group-tab} Ubuntu 2204, 2404
sudo apt update
sudo apt install libnginx-mod-http-brotli-filter libnginx-mod-http-brotli-static
:::
:::{group-tab} CentOS
WIP
:::
:::{group-tab} Docker
Pull a custom dockerfile

```bash
mkdir nginx
curl -o my-nginx/Dockerfile https://raw.githubusercontent.com/nginxinc/docker-nginx/master/modules/Dockerfile
```

Replace the nginx service in your docker-compose as follows

```dockerfile
  nginx:
    build:
      context: ./nginx/
      args:
        ENABLED_MODULES: brotli
    restart: always
    volumes:
      - ./conf/nginx.conf:/etc/nginx/nginx.conf
      - static-volume:/var/www/myauth/static
    depends_on:
      - allianceauth_gunicorn
    logging:
      driver: "json-file"
      options:
        max-size: "10Mb"
        max-file: "5"
```

:::
::::

Modify your nginx.conf as follows

```conf
load_module modules/ngx_http_brotli_static_module.so;
load_module modules/ngx_http_brotli_filter_module.so;
...
http {
  ...
    server {
        ...
        location /static {
            ...
            brotli_static on;
            brotli_types application/javascript text/css font/woff2 image/png image/svg+xml font/woff image/gif;
            brotli_comp_level 11;
        }
        ...
        location / {
            ...
            brotli on;
            brotli_comp_level 4;
        }
    }
}
```

### Staticfile Pre-Compression

We can use a small library to pre-compress staticfiles for Nginx to deliver.

```shell
pip install django-static-compress
```

Add the following lines to local.py

```python
# Tuning / Compression
STORAGES = {
    "staticfiles": {
        "BACKEND": "static_compress.CompressedStaticFilesStorage",
    },
}

STATIC_COMPRESS_FILE_EXTS = ['js', 'css', 'woff2', 'png', 'svg', 'woff', 'gif']
STATIC_COMPRESS_METHODS = ['gz', 'br']
STATIC_COMPRESS_KEEP_ORIGINAL = True
STATIC_COMPRESS_MIN_SIZE_KB = 1
```

## Cloudflare

### Brotli E2E Compression

Soon to be turned on by default. Refer to <https://developers.cloudflare.com/speed/optimization/content/brotli/enable/>

In order for cloudflare to seamlessly pass on your brotli compressed pages (End to End), ensure minification, rocket loader and other features are _off_ <https://developers.cloudflare.com/speed/optimization/content/brotli/enable/#notes-about-end-to-end-compression>. Else cloudflare will need to uncompress, modify, then recompress your pages.
