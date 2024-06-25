# Tuning

The official installation guide will install a stable version of Alliance Auth that will work fine for most cases. However, there are a lot of levels that can be used to optimize a system. For example, some installations may we short on RAM and want to reduce the total memory footprint, even though that may reduce system performance. Others are fine with further increasing the memory footprint to get better system performance.

:::{warning}
Tuning usually has benefits and costs and should only be performed by experienced Linux administrators who understand the impact of tuning decisions on their system.
:::

:::{toctree}
:maxdepth: 1

gunicorn
celery
redis
python
sql
:::
