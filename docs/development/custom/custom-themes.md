# Theme Hooks

The theme hook allows custom themes to be loaded dynamically by AAs CSS/JS Bundles, as selected by Users.

To register a ThemeHook class you would do the following:

```python
@hooks.register('theme_hook')
def register_darkly_hook():
    return ThemeHook()
```

The `ThemeHook` class specifies some parameters/instance variables required.

```{eval-rst}
.. autoclass:: allianceauth.theme.hooks.ThemeHook
    :members: __init__
    :undoc-members:
```
