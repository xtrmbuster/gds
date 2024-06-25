# Permissions Auditing

Access to most of Alliance Auth's features is controlled by Django's permissions system. To help you secure your services, Alliance Auth provides a permission auditing tool.

This is an optional app that needs to be installed.

To install it add `'allianceauth.permissions_tool',` to your `INSTALLED_APPS` list in your auth project's settings file.

## Usage

### Access

To grant users access to the permission auditing tool, they will need to be granted the `permissions_tool.audit_permissions` permission or be a superuser.

When a user has access to the tool, they will see the "Permissions Audit" menu item.

### Permissions Overview

The first page gives you a general overview of permissions and how many users have access to each permission.

![permissions overview](/_static/images/features/apps/permissions_tool/overview.png)

**App**, **Model** and **Code Name** contain the internal details of the permission while **Name** contains the name/description you'll see in the admin panel.

**Users** is the number of users explicitly granted this permission on their account.

**Groups** is the number of groups with this permission assigned.

**Groups Users** is the total number of users in all of the groups with this permission assigned.

Clicking on the **Code Name** link will take you to the [Permissions Audit Page](#permissions-audit-page)

### Permissions Audit Page

The permissions audit page will give you an overview of all the users who have access to this permission either directly or granted via group membership.

![permissions audit](/_static/images/features/apps/permissions_tool/audit.png)

Please note that users may appear multiple times if this permission is granted via multiple sources.

## Permissions

To use this feature, users will require some of the following.

```{eval-rst}
+---------------------------------------+------------------+--------------------------------------------------------------------------+
| Permission                            | Admin Site       | Auth Site                                                                |
+=======================================+==================+==========================================================================+
| permissions_tool.audit_permissions    | None             | Can view the Permissions Audit tool                                      |
+---------------------------------------+------------------+--------------------------------------------------------------------------+
```
