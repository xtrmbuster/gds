# Apache

## Overview

Alliance Auth gets served using a Web Server Gateway Interface (WSGI) script. This script passes web requests to Alliance Auth, which generates the content to be displayed and returns it. This means very little has to be configured in Apache to host Alliance Auth.

If you're using a small VPS to host services with very limited memory, consider using [NGINX](nginx.md).

## Installation

::::{tabs}

:::{group-tab} Ubuntu 2004, 2204

```shell
apt-get install apache2
```

:::
:::{group-tab} CentOS 7

```shell
yum install httpd
```

:::
:::{group-tab} CentOS Stream 8

```shell
dnf install httpd
```

:::
:::{group-tab} CentOS Stream 9

```shell
systemctl enable httpd
systemctl start httpd
```

:::
::::

CentOS 7, Stream 8, Stream 9

## Configuration

### Permissions

Apache needs to be able to read the folder containing your auth project's static files.

::::{tabs}
:::{group-tab} Ubuntu 2004, 2204

```shell
chown -R www-data:www-data /var/www/myauth/static
```

:::
:::{group-tab} CentOS 7

```shell
chown -R apache:apache /var/www/myauth/static
```

:::
:::{group-tab} CentOS Stream 8

```shell
chown -R apache:apache /var/www/myauth/static
```

:::
:::{group-tab} CentOS Stream 9

```shell
chown -R apache:apache /var/www/myauth/static
```

:::
::::

### Further Configuration

Apache serves sites through defined virtual hosts. These are located in `/etc/apache2/sites-available/` on Ubuntu and `/etc/httpd/conf.d/httpd.conf` on CentOS.

A virtual host for auth needs only proxy requests to your WSGI server (Gunicorn if you followed the installation guide) and serve static files. Examples can be found below. Create your config in its own file e.g. `myauth.conf`

::::{tabs}
:::{group-tab} Ubuntu 2004, 2204
To proxy and modify headers a few mods need to be enabled.

```shell
a2enmod proxy
a2enmod proxy_http
a2enmod headers
```

Create a new config file for auth e.g. `/etc/apache2/sites-available/myauth.conf` and fill out the virtual host configuration. To enable your config use `a2ensite myauth.conf` and then reload apache with `service apache2 reload`.
:::
:::{group-tab} CentOS 7
Place your virtual host configuration in the appropriate section within `/etc/httpd/conf.d/httpd.conf` and restart the httpd service with `systemctl restart httpd`.
:::
:::{group-tab} CentOS Stream 8
Place your virtual host configuration in the appropriate section within `/etc/httpd/conf.d/httpd.conf` and restart the httpd service with `systemctl restart httpd`.
:::
:::{group-tab} CentOS Stream 9
Place your virtual host configuration in the appropriate section within `/etc/httpd/conf.d/httpd.conf` and restart the httpd service with `systemctl restart httpd`.
:::
::::

:::{warning}
In some scenarios, the Apache default page is still enabled. To disable it use

```shell
a2dissite 000-default.conf
```

:::

### CentOS

## Sample Config File

```ini
<VirtualHost *:80>
        ServerName auth.example.com

        ProxyPassMatch ^/static !
        ProxyPassMatch ^/robots.txt !
        ProxyPassMatch ^/favicon.ico !

        ProxyPass / http://127.0.0.1:8000/
        ProxyPassReverse / http://127.0.0.1:8000/
        ProxyPreserveHost On

        Alias "/static" "/var/www/myauth/static"
        Alias "/robots.txt" "/var/www/myauth/static/robots.txt"
        Alias "/favicon.ico" "/var/www/myauth/static/allianceauth/icons/favicon.ico"

        <Directory "/var/www/myauth/static">
            Require all granted
        </Directory>

        <Location "/robots.txt">
            SetHandler None
            Require all granted
        </Location>

        <Location "/favicon.ico">
            SetHandler None
            Require all granted
        </Location>
</VirtualHost>
```

## SSL

It's 2018 - there's no reason to run a site without SSL. The EFF provides free, renewable SSL certificates with an automated installer. Visit their [website](https://certbot.eff.org/) for information.

After acquiring SSL, the config file needs to be adjusted. Add the following lines inside the `<VirtualHost>` block:

```ini
        RequestHeader set X-FORWARDED-PROTOCOL https
        RequestHeader set X-FORWARDED-SSL On
```

### Known Issues

#### Apache2 vs. Django

For some versions of Apache2, you might have to tell the Django framework explicitly
to use SSL, since the automatic detection doesn't work. SSL in general will work,
but internally created URLs by Django might still be prefixed with just `http://`
instead of `https://`, so it can't hurt to add these lines to
`myauth/myauth/settings/local.py`.

```python
# Setup support for proxy headers
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")
```
