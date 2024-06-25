# Templates

## Bundles

As bundles, we see templates that load essential CSS and JavaScript and are used
throughout Alliance Auth. These bundles can also be used in your own apps, so you don't
have to load specific CSS or JavaScript yourself.

These bundles include DataTables CSS and JS, jQuery Datepicker CSS and JS, jQueryUI CSS and JS, and more.

A full list of bundles we provide can be found here: <https://gitlab.com/allianceauth/allianceauth/-/tree/master/allianceauth/templates/bundles>

To use a bundle, you can use the following code in your template (Example for jQueryUI):

```django
{% block extra_css %}
    {% include "bundles/jquery-ui-css.html" %}
{% endblock %}

{% block extra_javascript %}
    {% include "bundles/jquery-ui-js.html" %}
{% endblock %}
```

## Template Partials

To ensure a unified style language throughout Alliance Auth and Community Apps,
we also provide a couple of template partials. This collection is bound to grow over
time, so best have an eye on this page.

### Dashboard Widget Title

To ensure the dashboard widgets have a unified style, we provide a template partial for the widget title.

To use it, you can use the following code in your dashboard widget template:

```django
<div id="my-app-dashboard-widget" class="col-12 mb-3">
    <div class="card">
        <div class="card-body">
            {% translate "My Widget Title" as widget_title %}
            {% include "framework/dashboard/widget-title.html" with title=widget_title %}

            <div>
                <p>My widget content</p>
            </div>
        </div>
    </div>
</div>
```

### Page Header

On some pages you want to have a page header. To make this easier, we provide a template partial for this.

To use it, you can use the following code in your template:

```django
{% block content %}
    <div>
        {% translate "My Page Header" as page_header %}
        {% translate "My Page Header Subtitle" as optional_subtitle %}
        {% include "framework/header/page-header.html" with title=page_header subtitle=optional_subtitle %}

        <p>My page content</p>
    </div>
{% endblock %}
```
