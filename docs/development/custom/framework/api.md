# Alliance Auth Helper-Functions API

The following helper-functions are available in the `allianceauth.framework.api` module.
They are intended to be used in Alliance Auth itself as well as in the community apps.

These functions are intended to make the life of our community apps developer a little
easier, so they don't have to reinvent the wheel all the time.

## EveCharacter API

### get_main_character_from_evecharacter

This is to get the main character object (`EveCharacter`) of an `EveCharacter` object.

Given we have an `EveCharacter` object called `my_evecharacter` and we want to get the main character:

```python
# Alliance Auth
from allianceauth.framework.api.evecharacter import get_main_character_from_evecharacter

main_character = get_main_character_from_evecharacter(character=my_evecharacter)
```

Now, `main_character` is an `EveCharacter` object, or `None` if the `EveCharacter` has no main character.

### get_user_from_evecharacter

This is to get the user object (`User`) of an `EveCharacter` object.

Given we have an `EveCharacter` object called `my_evecharacter` and we want to get the user:

```python
# Alliance Auth
from allianceauth.framework.api.evecharacter import get_user_from_evecharacter

user = get_user_from_evecharacter(character=my_evecharacter)
```

Now, `user` is a `User` object, or the sentinel username (see [get_sentinel_user](#get_sentinel_user))
if the `EveCharacter` has no user.

## User API

### get_all_characters_from_user

This is to get all character objects (`EveCharacter`) of a user.

Given we have a `User` object called `my_user` and we want to get all characters:

```python
# Alliance Auth
from allianceauth.framework.api.user import get_all_characters_from_user

characters = get_all_characters_from_user(user=my_user)
```

Now, `characters` is a `list` containing all `EveCharacter` objects of the user.
If the user is `None`, an empty `list` will be returned.

### get_main_character_from_user

This is to get the main character object (`EveCharacter`) of a user.

Given we have a `User` object called `my_user` and we want to get the main character:

```python
# Alliance Auth
from allianceauth.framework.api.user import get_main_character_from_user

main_character = get_main_character_from_user(user=my_user)
```

Now, `main_character` is an `EveCharacter` object, or `None` if the user has no main
character or the user is `None`.

### get_main_character_name_from_user

This is to get the name of the main character from a user.

Given we have a `User` object called `my_user` and we want to get the main character name:

```python
# Alliance Auth
from allianceauth.framework.api.user import get_main_character_name_from_user

main_character = get_main_character_name_from_user(user=my_user)
```

Now, `main_character` is a `string` containing the user's main character name.
If the user has no main character, the username will be returned. If the user is `None`,
the sentinel username (see [get_sentinel_user](#get_sentinel_user)) will be returned.

### get_sentinel_user

This function is useful in models when using `User` model-objects as foreign keys.
Django needs to know what should happen to those relations when the user is being
deleted. To keep the data, you can have Django map this to the sentinel user.

Import:

```python
# Alliance Auth
from allianceauth.framework.api.user import get_sentinel_user
```

And later in your model:

```python
creator = models.ForeignKey(
    to=User,
    on_delete=models.SET(get_sentinel_user),
)
```
