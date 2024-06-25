# Upgrading Python 3

This guide describes how to upgrade an existing Alliance Auth (AA) installation to a newer Python 3 version.

This guide shares many similarities with the Alliance Auth install guide, but it is targeted towards existing installations needing to update.

:::{note}
This guide will upgrade the software components only but not change any data or configuration.
:::

## Install a new Python version

To run AA with a newer Python 3 version than your system's default, you need to install it first. Technically, it would be possible to upgrade your system's default Python 3, but since many of your system's tools have been tested to work with that specific version, we would not recommend it. Instead, we recommend installing an additional Python 3 version alongside your default version and using that for AA.

To install other Python versions than those included with your distribution, you need to add a new installation repository. Then you can install the specific Python 3 to your system.

:::{note}
Ubuntu 2204 ships with Python 3.10 already
:::

Centos Stream 8/9:
:::{note}
A Python 3.9 Package is available for Stream 8 and 9. You _may_ use this instead of building your own package. But our documentation will assume Python3.11, and you may need to substitute as necessary
sudo dnf install python39 python39-devel
:::

::::{tabs}
:::{group-tab} Ubuntu 2004, 2204

```shell
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.11 python3.11-dev python3.11-venv
```

:::
:::{group-tab} CentOS 7

```bash
cd ~
sudo yum install gcc openssl-devel bzip2-devel libffi-devel wget
wget https://www.python.org/ftp/python/3.11.7/Python-3.11.7.tgz
tar xvf Python-3.11.7.tgz
cd Python-3.11.7/
./configure --enable-optimizations --enable-shared
sudo make altinstall
```

:::
:::{group-tab} CentOS Stream 8

```bash
cd ~
sudo yum install gcc openssl-devel bzip2-devel libffi-devel wget
wget https://www.python.org/ftp/python/3.11.7/Python-3.11.7.tgz
tar xvf Python-3.11.7.tgz
cd Python-3.11.7/
./configure --enable-optimizations --enable-shared
sudo make altinstall
```

:::
:::{group-tab} CentOS Stream 9

```bash
cd ~
sudo yum install gcc openssl-devel bzip2-devel libffi-devel wget
wget https://www.python.org/ftp/python/3.11.7/Python-3.11.7.tgz
tar xvf Python-3.11.7.tgz
cd Python-3.11.7/
./configure --enable-optimizations --enable-shared
sudo make altinstall
```

:::
::::

## Preparing your venv

Before updating your venv, it is important to make sure that your current installation is stable. Otherwise, your new venv might not be consistent with your data, which might create problems.

Start by navigating to your main project folder (the one that has `manage.py` in it). If you followed the default installation, the path is: `/home/allianceserver/myauth`

:::{note}
If you installed Alliance Auth under the allianceserver user, as recommended. Remember to switch users for easier permission management::
:::

```bash
sudo su allianceserver
```

Activate your venv:

```shell
source /home/allianceserver/venv/auth/bin/activate
```

### Upgrade AA

Make sure to upgrade AA to the newest version:

```shell
pip install -U allianceauth
```

Run migrations and collectstatic.

```shell
python manage.py migrate
```

```shell
python manage.py collectstatic
```

Restart your AA supervisor:

```shell
supervisorctl restart myauth:
```

### Upgrade your apps

You also need to upgrade all additional apps to their newest version that you have installed. And you need to make sure that you can reinstall all your apps later, e.g., you know from which repo they came. We recommend making a list of all your apps, so you can go through them later when you rebuild your venv.

If you unsure which apps you have installed from repos check `INSTALLED_APPS` in your settings. Alternatively, run this command to get a list of all apps in your venv.

```shell
pip list
```

Repeat as needed for your apps

```shell
pip install -U APP_NAME
```

Make sure to run migrations and collect static files for all upgraded apps.

```shell
python manage.py migrate
```

```shell
python manage.py collectstatic
```

### Restart and final check

Do a final restart of your AA supervisors and make sure your installation is still running normally.

For a final check that there are no issues - e.g., any outstanding migrations - run this command:

```shell
python manage.py check
```

If you get the following result, you are good to go. Otherwise, make sure to fix any issues first before proceeding.

```shell
System check identified no issues (0 silenced).
```

## Backup current venv

Make sure you are in your venv!

First, we create a list of all installed packages in your venv. You can use this list later as a reference to see what packages should be installed.

```shell
pip freeze > requirements.txt
```

At this point, we recommend creating a list of the additional packages that you need to manually reinstall later on top of AA:

- Community AA apps (e.g. aa-structures)
- Additional tools you are using (e.g., flower, django-extensions)

:::{hint}
While `requirements.txt` will contain a complete list of your packages, it will also contain many packages that are automatically installed as dependencies and don't need to be manually reinstalled.
:::
:::{note}
Some guides on the Internet will suggest using the `requirements.txt` file to recreate a venv. This is indeed possible, but only works if all packages can be installed from PyPI. Since most community apps are installed directly from repos, this guide will not follow that approach.
:::

Leave the venv and shutdown all AA services:

```shell
deactivate
```

```shell
supervisorctl stop myauth:
```

Rename and keep your old venv, so we have a fallback in case of some unforeseeable issues:

```shell
mv /home/allianceserver/venv/auth /home/allianceserver/venv/auth_old
```

## Create your new venv

Now let's create our new venv with Python 3.11 and activate it:

```shell
python3.11 -m venv /home/allianceserver/venv/auth
```

```shell
source /home/allianceserver/venv/auth/bin/activate
```

## Reinstall packages

Now we need to reinstall all packages into your new venv.

### Install basic packages

```shell
pip install -U pip setuptools wheel
```

### Installing AA & Gunicorn

```shell
pip install allianceauth
```

```shell
pip install gunicorn
```

### Install all other packages

Last, but not least, you need to reinstall all other packages, e.g., for AA community apps or additional tools.

Use the list of packages you created earlier as a checklist. Alternatively you use the `requirements.txt` file we created earlier to see what you need. During the installation process you can run `pip list` to see what you already got installed.

To check whether you are missing any apps, you can also run the check command:

```shell
python manage.py check
```

Note: In case you forget to install an app, you will get this error

```shell
ModuleNotFoundError: No module named 'xyz'
```

Note that you should not need to run any migrations unless you forgot to upgrade one of your existing apps, or you got the newer version of an app through a dependency. In that case, you run migrations normally.

## Restart

After you have completed installing all packages, start your AA supervisor again.

```shell
supervisorctl start myauth:
```

We recommend keeping your old venv copy for a couple of days, so you have a fallback just in case. After that, you should be fine to remove it.

## Fallback

In case you run into any major issue, you can always switch back to your initial venv.

Before you start double-check that you still have your old venv for auth:

```shell
ls /home/allianceserver/venv/auth /home/allianceserver/venv
```

If the output shows these two folders, you should be safe to proceed:

- `auth`
- `auth_old`

Run these commands to remove your current venv and switch back to the old venv for auth:

```shell
supervisorctl stop myauth:
```

```shell
rm -rf /home/allianceserver/venv/auth
```

```shell
mv /home/allianceserver/venv/auth_old /home/allianceserver/venv/auth
```

```shell
supervisorctl start myauth:
```
