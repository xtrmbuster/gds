# Alliance Auth

[![license](https://img.shields.io/badge/license-GPLv2-green)](https://pypi.org/project/allianceauth/)
[![python](https://img.shields.io/pypi/pyversions/allianceauth)](https://pypi.org/project/allianceauth/)
[![django](https://img.shields.io/pypi/djversions/allianceauth?label=django)](https://pypi.org/project/allianceauth/)
[![version](https://img.shields.io/pypi/v/allianceauth?label=release)](https://pypi.org/project/allianceauth/)
[![pipeline status](https://gitlab.com/allianceauth/allianceauth/badges/master/pipeline.svg)](https://gitlab.com/allianceauth/allianceauth/commits/master)
[![Documentation Status](https://readthedocs.org/projects/allianceauth/badge/?version=latest)](http://allianceauth.readthedocs.io/?badge=latest)
[![coverage report](https://gitlab.com/allianceauth/allianceauth/badges/master/coverage.svg)](https://gitlab.com/allianceauth/allianceauth/commits/master)
[![Chat on Discord](https://img.shields.io/discord/399006117012832262.svg)](https://discord.gg/fjnHAmk)

An auth system for EVE Online to help in-game organizations manage online service access.

## Content

- [Overview](#overview)
- [Documentation](http://allianceauth.rtfd.io)
- [Support](#support)
- [Release Notes](https://gitlab.com/allianceauth/allianceauth/-/releases)
- [Developer Team](#development-team)
- [Contributing](#contributing)

## Overview

Alliance Auth (AA) is a web site that helps Eve Online organizations efficiently manage access to applications and services.

Main features:

- Automatically grants or revokes user access to external services (e.g. Discord, Mumble) and web apps (e.g. SRP requests) based on the user's current membership to [in-game organizations](https://allianceauth.readthedocs.io/en/latest/features/core/states/) and [groups](https://allianceauth.readthedocs.io/en/latest/features/core/groups/)

- Provides a central web site where users can directly access web apps (e.g. SRP requests, Fleet Schedule) and manage their access to external services and groups.

- Includes a set of connectors (called ["services"](https://allianceauth.readthedocs.io/en/latest/features/services/)) for integrating access management with many popular external applications / services like Discord, Mumble, Teamspeak 3, SMF and others

- Includes a set of web [apps](https://allianceauth.readthedocs.io/en/latest/features/apps/) which add many useful functions, e.g.: fleet schedule, timer board, SRP request management, fleet activity tracker

- Can be easily extended with additional services and apps. Many are provided by the community and can be found here: [Community Creations](https://gitlab.com/allianceauth/community-creations)

- English :flag_gb:, Chinese :flag_cn:, German :flag_de:, Spanish :flag_es:, Korean :flag_kr:, Russian :flag_ru:, Italian :flag_it:, French :flag_fr:, Japanese :flag_jp: and Ukrainian :flag_ua: Localization

For further details about AA - including an installation guide and a full list of included services and plugin apps - please see the [official documentation](http://allianceauth.rtfd.io).

## Screenshot

Here is an example of the Alliance Auth web site with some plug-ins apps and services enabled:

![screenshot](https://i.imgur.com/2tnX9kD.png)

## Support

[Get help on Discord](https://discord.gg/fjnHAmk) or submit an [issue](https://gitlab.com/allianceauth/allianceauth/issues).

## Development Team

### Active Developers

- [Aaron Kable](https://gitlab.com/aaronkable/)
- [Ariel Rin](https://gitlab.com/soratidus999/)
- [Col Crunch](https://gitlab.com/colcrunch/)
- [Erik Kalkoken](https://gitlab.com/ErikKalkoken/)
- [Rounon Dax](https://gitlab.com/ppfeufer)
- [snipereagle1](https://gitlab.com/mckernanin)

### Former Developers

- [Adarnof](https://gitlab.com/adarnof/)
- [Basraah](https://gitlab.com/basraah/)

### Beta Testers / Bug Fixers

- [ghoti](https://gitlab.com/ChainsawMcGinny/)
- [kaezon](https://github.com/kaezon/)
- [mmolitor87](https://gitlab.com/mmolitor87/)
- [orbitroom](https://github.com/orbitroom/)
- [TargetZ3R0](https://github.com/TargetZ3R0)
- [tehfiend](https://github.com/tehfiend/)

Special thanks to [Nikdoof](https://github.com/nikdoof/), as his [auth](https://github.com/nikdoof/test-auth) was the foundation for the original work on this project.

## Contributing

Alliance Auth is maintained and developed by the community and we welcome every contribution!

To see what needs to be worked on please review our issue list or chat with our active developers on Discord.

Also, please make sure you have signed the [License Agreement](https://developers.eveonline.com/resource/license-agreement) by logging in at [https://developers.eveonline.com](https://developers.eveonline.com) before submitting any pull requests.

In addition to the core AA system we also very much welcome contributions to our growing list of 3rd party services and plugin apps. Please see [AA Community Creations](https://gitlab.com/allianceauth/community-creations) for details.
