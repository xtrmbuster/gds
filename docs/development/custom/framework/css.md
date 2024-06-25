# CSS Framework

To establish a unified style language throughout Alliance Auth and Community Apps,
Alliance Auth is providing its own CSS framework with a couple of CSS classes.

## Cursors

Our CSS framework provides different classes to manipulate the cursor, which are
missing in Bootstrap.

```{eval-rst}
+----------------------+--------------------------------------------------------+--------------------------------------------------------------------------------+
| CSS Class            | Effect                                                 | Example                                                                        |
+======================+========================================================+================================================================================+
| `cursor-default`     | System default curser                                  | .. image:: /_static/images/development/aa-framework/css/cursor-default.png     |
+----------------------+--------------------------------------------------------+--------------------------------------------------------------------------------+
| `cursor-pointer`     | Pointer, like it looks like for links and form buttons | .. image:: /_static/images/development/aa-framework/css/cursor-pointer.png     |
+----------------------+--------------------------------------------------------+--------------------------------------------------------------------------------+
| `cursor-wait`        | Wait animation                                         | .. image:: /_static/images/development/aa-framework/css/cursor-wait.png        |
+----------------------+--------------------------------------------------------+--------------------------------------------------------------------------------+
| `cursor-text`        | Text selection cursor                                  | .. image:: /_static/images/development/aa-framework/css/cursor-text.png        |
+----------------------+--------------------------------------------------------+--------------------------------------------------------------------------------+
| `cursor-move`        | 4-arrow-shaped cursor                                  | .. image:: /_static/images/development/aa-framework/css/cursor-move.png        |
+----------------------+--------------------------------------------------------+--------------------------------------------------------------------------------+
| `cursor-help`        | Cursor with a little question mark                     | .. image:: /_static/images/development/aa-framework/css/cursor-help.png        |
+----------------------+--------------------------------------------------------+--------------------------------------------------------------------------------+
| `cursor-not-allowed` | Not Allowed sign                                       | .. image:: /_static/images/development/aa-framework/css/cursor-not-allowed.png |
+----------------------+--------------------------------------------------------+--------------------------------------------------------------------------------+
| `cursor-inherit`     | Inherited from its parent element                      |                                                                                |
+----------------------+--------------------------------------------------------+--------------------------------------------------------------------------------+
| `cursor-zoom-in`     | Zoom in symbol                                         | .. image:: /_static/images/development/aa-framework/css/cursor-zoom-in.png     |
+----------------------+--------------------------------------------------------+--------------------------------------------------------------------------------+
| `cursor-zoom-out`    | Zoom out symbol                                        | .. image:: /_static/images/development/aa-framework/css/cursor-zoom-out.png    |
+----------------------+--------------------------------------------------------+--------------------------------------------------------------------------------+
```

## Callout-Boxes

These are similar to the Bootstrap alert/notification boxes, but not as "loud".

Callout-boxes need a base-class (`.aa-callout`) and a modifier-class (e.g.:
`.aa-callout-info` for an info-box). Modifier classes are available for the usual
Bootstrap alert levels "Success", "Info", "Warning" and "Danger".

### HTML

```html
<div class="aa-callout">
    <p>
      This is a callout-box.
    </p>
</div>
```

![Alliance Auth Framework: Callout Boxes](/_static/images/development/aa-framework/css/callout-box.png "Alliance Auth Framework: Callout Boxe")

#### Alert Level Modifier Classes

The callout boxes come in four alert levels: success, info, warning and danger.

Use the modifier classes `.aa-callout-success`, `.aa-callout-info`, `.aa-callout-warning` and `.aa-callout-danger` to change the left border color of the callout box.

```html
<div class="aa-callout aa-callout-success">
    <p>
        This is a success callout-box.
    </p>
</div>

<div class="aa-callout aa-callout-info">
    <p>
        This is an info callout-box.
    </p>
</div>

<div class="aa-callout aa-callout-warning">
    <p>
        This is a warning callout-box.
    </p>
</div>

<div class="aa-callout aa-callout-danger">
    <p>
        This is a danger callout-box.
    </p>
</div>
```

![Alliance Auth Framework: Callout Boxes Alert Modifier](/_static/images/development/aa-framework/css/callout-boxes-alert-modifier.png "Alliance Auth Framework: Callout Boxes Alert Modifier")

#### Size Modifier Classes

The callout boxes come in three sizes: small, default and large.

Use the modifier classes `.aa-callout-sm` for small and `.aa-callout-lg` for large, where `.aa-callout-sm` will change the default padding form 1rem to 0.5rem and `.aa-callout-lg` will change it to 1.5rem.

These modifier classes can be combined with the alert level modifier classes.

```html
<div class="aa-callout aa-callout-sm">
    <p>
        This is a small callout-box.
    </p>
</div>

<div class="aa-callout">
    <p>
        This is a default callout-box.
    </p>
</div>

<div class="aa-callout aa-callout-lg">
    <p>
        This is a large callout-box.
    </p>
</div>
```

![Alliance Auth Framework: Callout Boxes Size Modifier](/_static/images/development/aa-framework/css/callout-boxes-size-modifier.png "Alliance Auth Framework: Callout Boxes Size Modifier")
