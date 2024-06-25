# Fleet Activity Tracking

The Fleet Activity Tracking (FAT) app allows you to track fleet participation.

![fat](/_static/images/features/apps/fat.png)

## Installation

Fleet Activity Tracking requires access to the `esi-location.read_location.v1`, `esi-location.read_ship_type.v1`, and `esi-universe.read_structures.v1` SSO scopes. Update your application on the [EVE Developers site](https://developers.eveonline.com) to ensure these are available.

Add `'allianceauth.fleetactivitytracking',` to your `INSTALLED_APPS` list in your auth project's settings file. Run migrations to complete installation.

## Permissions

To administer this feature, users will require some of the following.

Users do not require any permissions to interact with FAT Links created.

```{eval-rst}
+---------------------------------------+------------------+--------------------------------------------------------------------------+
| Permission                            | Admin Site       | Auth Site                                                                |
+=======================================+==================+==========================================================================+
| auth.fleetactivitytracking            | None             | Create and Modify FATLinks                                               |
+---------------------------------------+------------------+--------------------------------------------------------------------------+
| auth.fleetactivitytracking_statistics | None             | Can view detailed statistics for corp models and other characters.       |
+---------------------------------------+------------------+--------------------------------------------------------------------------+
```
