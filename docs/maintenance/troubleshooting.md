# Troubleshooting

## Logging

In its default configuration, your auth project logs INFO and higher messages to myauth/log/allianceauth.log. If you're encountering issues, it's a good idea to view DEBUG messages as these greatly assist the troubleshooting process. These are printed to the console with manually starting the webserver via `python manage.py runserver`.

To record DEBUG messages in the log file, alter a setting in your auth project's settings file: `LOGGING['handlers']['log_file']['level'] = 'DEBUG'`. After restarting gunicorn and celery, your log file will record all logging messages.

## Steps to Check Logs for Errors

### Locate the Logs

The logs are located within the `myauth/log/` directory of your Alliance Auth project.

### Access the Logs

Use a text editor or terminal commands (like `tail -f <filename>`) to open the relevant log files.

_(The `tail -f` command displays the last few lines of a file and then continues to monitor the file, printing any new lines that are added in real-time. Useful to watch while actively testing a troublesome feature while troubleshooting.)_

Consider the following:

`allianceauth.log` is the primary log for general troubleshooting. Tracks user actions, changes made, and potential errors.

`worker.log` is important for issues related to background tasks.(Such as services(Discord)).

`beat.log` if you suspect scheduler problems.

`gunicorn.log` for web-specific or Gunicorn worker errors.

### Search for Errors

Look for keywords like `ERROR`, `WARNING`, `EXCEPTION`, or `CRITICAL`. Examine timestamps to correlate errors with user actions or events. Read the error messages carefully for clues about the problem's nature.

Troubleshooting Tips:

**Filter Logs:** Use tools like `grep` to filter logs based on keywords or timeframes, making it easier to focus on relevant information.

**Example**: `tail -f worker.log | grep -i 'discord'`. This will isolate lines containing discord. Making it easier to see among the other logs.

**Debug Mode:** For in-depth troubleshooting, temporarily enable DEBUG logging in your `local.py` to get more detailed messages. Remember to set it back to `False` after debugging.

**Important Note: Before sharing logs publicly, sanitize any sensitive information such as usernames, passwords, or API keys.**

## Common Problems

### I'm getting error 500 when trying to connect to the website on a new installation

_Great._ Error 500 is the generic message given by your web server when _anything_ breaks. The actual error message is hidden in one of your auth project's log files. Read them to identify it.

### Failed to configure log handler

Make sure the log directory is writeable by the allianceserver user: `chmown -R allianceserver:allianceserver /path/to/myauth/log/`, then restart the auth supervisor processes.

### Groups aren't syncing to services

Make sure the background processes are running: `supervisorctl status myauth:`. If `myauth:worker` or `myauth:beat` do not show `RUNNING` read their log files to identify why.

### Task queue is way too large

Stop celery workers with `supervisorctl stop myauth:worker` then clear the queue:

```shell
redis-cli FLUSHALL
celery -A myauth worker --purge
```

Press Control+C once.

Now start the worker again with `supervisorctl start myauth:worker`

### Proxy timeout when entering email address

This usually indicates an issue with your email settings. Ensure these are correct and your email server/service is properly configured.

### No images are available to users accessing the website

This is likely due to a permission mismatch. Check the setup guide for your web server. Additionally ensure the user who owns `/var/www/myauth/static` is the same user as running your webserver, as this can be non-standard.

### Unable to execute 'gunicorn myauth.wsgi' or ImportError: No module named 'myauth.wsgi'

Gunicorn needs to have context for its running location, `/home/alllianceserver/myauth/gunicorn myauth.wsgi` will not work, instead `cd /home/alllianceserver/myauth` then `gunicorn myauth.wsgi` is needed to boot Gunicorn. This is handled in the Supervisor config, but this may be encountered running Gunicorn manually for testing.

### Specified key was too long error

Migrations may about with the following error message:

```shell
Specified key was too long; max key length is 767 bytes
```

This error will occur if one is trying to use Maria DB prior to 10.2.x, which is not compatible with Alliance Auth.

Install a newer Maria DB version to fix this issue another DBMS supported by Django 2.2.
