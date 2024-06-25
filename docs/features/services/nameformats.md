# Services Name Formats

This app allows you to customize how usernames for services are created.

Each service's username or nickname, depending on which the service supports, can be customized through the use of the Name Formatter config provided the service supports custom formats. This config can be found in the admin panel under **Services -> Name format config**

Currently, the following services support custom name formats:

```{eval-rst}
+-------------+-----------+-------------------------------------+
| Service     | Used with | Default Formatter                   |
+=============+===========+=====================================+
| Discord     | Nickname  | ``{character_name}``                |
+-------------+-----------+-------------------------------------+
| Discourse   | Username  | ``{character_name}``                |
+-------------+-----------+-------------------------------------+
| IPS4        | Username  | ``{character_name}``                |
+-------------+-----------+-------------------------------------+
| Mumble      | Username  | ``[{corp_ticker}]{character_name}`` |
+-------------+-----------+-------------------------------------+
| Openfire    | Username  | ``{character_name}``                |
+-------------+-----------+-------------------------------------+
| phpBB3      | Username  | ``{character_name}``                |
+-------------+-----------+-------------------------------------+
| SMF         | Username  | ``{character_name}``                |
+-------------+-----------+-------------------------------------+
| Teamspeak 3 | Nickname  | ``[{corp_ticker}]{character_name}`` |
+-------------+-----------+-------------------------------------+
| Xenforo     | Username  | ``{character_name}``                |
+-------------+-----------+-------------------------------------+
```

:::{note}
It's important to note here, before we get into what you can do with a name formatter, that before the generated name is passed off to the service to create an account it will be sanitized to remove characters (the letters and numbers etc.) that the service cannot support. This means that, despite what you configured, the service may display something different. It is up to you to test your formatter and understand how your format may be disrupted by a certain services sanitization function.
:::

## Available format data

The following fields are available for a user account and main character:

- `username` - Alliance Auth username
- `character_id`
- `character_name`
- `corp_id`
- `corp_name`
- `corp_ticker`
- `alliance_id`
- `alliance_name`
- `alliance_ticker`
- `alliance_or_corp_name` (defaults to Corporation name if there is no Alliance)
- `alliance_or_corp_ticker` (defaults to Corporation ticker if there is no Alliance)

## Building a formatter string

The name formatter uses the advanced string formatting specified by [PEP-3101](https://www.python.org/dev/peps/pep-3101/). Anything supported by this specification is supported in a name formatter.

More digestible documentation of string formatting in Python is available on the [PyFormat](https://pyformat.info/) website.

Some examples of strings you could use:

```{eval-rst}
+------------------------------------------+---------------------------+
| Formatter                                | Result                    |
+==========================================+===========================+
| ``{alliance_ticker} - {character_name}`` | ``MYALLI - My Character`` |
+------------------------------------------+---------------------------+
| ``[{corp_ticker}] {character_name}``     | ``[CORP] My Character``   |
+------------------------------------------+---------------------------+
| ``{{{corp_name}}}{character_name}``      | ``{My Corp}My Character`` |
+------------------------------------------+---------------------------+
```

:::{important}
For most services, name formats only take effect when a user creates an account. This means if you create or update a name formatter, it won't retroactively alter the format of users' names. There are some exceptions to this where the service updates nicknames on a periodic basis. Check the service's documentation to see which of these apply.
:::

:::{important}
You must only create one formatter per service per state. E.g., don't create two formatters for Mumble for the Member state. In this case, one of the formatters will be used, and it may not be the formatter you are expecting:
:::
