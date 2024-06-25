# SQL

SQL Tuning is usually the realm of experienced Database Admins, as it can be full of missteps leading to worse performance. It is _extremely_ important that you take it slowly, make one change at a time with dedicated research and test before and after.

Before you start down this path, it's best to update [MariaDB](https://mariadb.org/download/?t=repo-config) / MySQL. Performance Schemas, some default tuning and other general performance improvements are only available on new versions. You must also allow your server to run for 24 hours at least to gather accurate data.

## MySQLTuner

[MySQLTuner](https://github.com/major/MySQLTuner-perl) is a Perl script that will analyze inbuilt metrics and provide recommendations.

### [performance_schema](https://mariadb.com/kb/en/performance-schema-system-variables/#performance_schema)

This should be ON for 24 hours before applying any recommendations, then can be turned _OFF_ to save Memory while it's not needed.

```bash
-------- Performance schema ------------------------------------------------------------------------
[--] Performance_schema is activated.
[--] Memory used by Performance_schema: 105.7M
[--] Sys schema is installed.
# 105M could be significant depending on your hardware
```

## SQL Variables

### [skip-name-resolve](https://mariadb.com/kb/en/server-system-variables/#skip_name_resolve)

While on, SQL will perform a dns resolve for all connections, if your database is connected via IP, this will save you a handful of cpu cycles per connection.

Note you must use 127.0.0.1 for localhost connections, and all entries in GRANT tables (permissions), must use IP addresses.

### [table_definition_cache](https://mariadb.com/kb/en/server-system-variables/#table_definition_cache)

Usually need to be expanded on installations with many extensions.

Most installs should cache all their tables, but if your hit rate is still quite high, you may have a lot of rarely used tables that you don't need to waste memory caching.

```bash
[OK] Table cache hit rate: 63% (2K hits / 4K requests).
# Only 63% of our queries are using this cache
table_definition_cache (400) > 567 or -1 (autosizing if supported)
# Here We have 567 tables, but a default cache of only 400.
```

```bash
[OK] Table cache hit rate: 99% (372M hits / 372M requests)
[OK] table_definition_cache (600) is greater than number of tables (567)
# Much better
```

### [innodb_buffer_pool_size](https://mariadb.com/kb/en/innodb-system-variables/#innodb_buffer_pool_size)

This is in short, the amount of memory assigned to store data for faster reads. If you are memory starved, you should not increase this variable regardless of the suggestions of this tool. Pushing SQL cache to pagefile will not result in faster queries.

If you are not memory starved, you can wind this up to the amount of total data you have to store it all in memory. This would be a significant performance increase for larger installations on dedicated hardware with memory to spare.

```bash
[!!] InnoDB buffer pool / data size: 128.0M / 651.6M
# I have 651mb of _possible_ data to cache.
# We won't and shouldn't cache it all unless we have excess memory to spare.
...
[!!] InnoDB Read buffer efficiency: 0% (-2019 hits / 0 total)
# A low ratio here would suggest more Memory can be used effectively.
# A high ratio might mean we have most of our regularly used data cached already
```

### [innodb_log_buffer_size](https://mariadb.com/kb/en/innodb-system-variables/#innodb_log_buffer_size) / [innodb_log_file_size](https://mariadb.com/kb/en/innodb-system-variables/#innodb_log_file_size)

[innodb_log_file_size](https://mariadb.com/kb/en/innodb-system-variables/#innodb_log_file_size) This is your _write_ log, used to redo any commits in the event of a crash. MySQLTuner recommends this be 1/4 of your innodb_buffer_pool / read buffer. I would not lower this past the default size.

[innodb_log_buffer_size](https://mariadb.com/kb/en/innodb-system-variables/#innodb_log_buffer_size) This is the memory buffer for the "write" log. Larger transactions will benefit from a larger setting.

```bash
[!!] Ratio InnoDB log file size / InnoDB Buffer pool size (75%): 96.0M \* 1 / 128.0M should be equal to 25%
# Here our write log file is 75% of our read buffer, but 96MB is the default so we probably wont shrink it further
...
[OK] InnoDB Write Log efficiency: 99.11% (23167614 hits / 23375465 total) # Our transactions are typically not large enough to exhaust the write log buffer,
[OK] InnoDB log waits: 0.00% (0 waits / 207851 writes)
```

### [innodb_file_per_table](https://mariadb.com/kb/en/innodb-system-variables/#innodb_file_per_table)

This is not for performance, but for file system utilization and ease of use. While off, all tables are stored in a single monolith file, as opposed to individual files. This is deprecated and set to ON in MariaDB 11.x

```bash
[OK] InnoDB File per table is activated
```

### [join_buffer_size](https://mariadb.com/kb/en/server-system-variables/#join_buffer_size)

It is always better to optimize a table with indexes, if you have valuable performance data and analysis, please reach out to either the Alliance Auth or Community dev responsible for the data that could benefit from indexes. MySQLTuner will likely recommend increasing this number for as long as there are any queries that could benefit, regardless of their resulting performance impact.

Also keep in mind this is _per thread_, if you have a potential 200 connections, 256KB * 200 = 50MB, scaling this setting out too far can result in more memory use than expected.

```bash
[!!] Joins performed without indexes: 67646
```

```bash
[OK] No joins without indexes
# An ideal scenario. With well designed apps this is possible with a default join buffer.
```

### [tmp_table_size](https://mariadb.com/kb/en/server-system-variables/#tmp_table_size) / [max_heap_table_size](https://mariadb.com/kb/en/server-system-variables/#max_heap_table_size)

If a temporary table must be created due to a lack of other optimizations or large queries, it may only be stored in memory under this size. Any larger and it is performed on disk reducing performance.

tmp_table_size and max_heap_table_size should be increased together.

```bash
[!!] Temporary tables created on disk: 32% (775 on disk / 2K total)
# 32% of my temp tables are performed on disk. If you increase this size, monitor if your performance improves.
# If it does not you may have data of a certain size that is impractical to cache, and you can reclaim this memory.
```

```bash
[OK] Temporary tables created on disk: 0% (5K on disk / 4M total)
# Here only a miniscule amount of my temp tables are done on disk. No action required
```

### key_buffer_size

Index buffer for MyISAM tables, If you use no or very little data in MyISAM tables. You may reclaim some memory here

In this example, we still have some MyISAM tables. You may have none.

```bash
[--] General MyIsam metrics:
[--]  +-- Total MyISAM Tables  : 67
[--]  +-- Total MyISAM indexes : 7.1M
[--]  +-- KB Size :8.0M
[--]  +-- KB Used Size :1.5M
[--]  +-- KB used :18.3%
[--]  +-- Read KB hit rate: 0% (0 cached / 0 reads)
[--]  +-- Write KB hit rate: 0% (0 cached / 0 writes)
[!!] Key buffer used: 18.3% (1.5M used / 8.0M cache) # We have only filled 1.5M of the 8 assigned
[OK] Key buffer size / total MyISAM indexes: 8.0M/7.1M # This is the max theoretical buffer to cache all my indexes
Variables to adjust:
  key_buffer_size (~ 1M)
# Tuner has seen that we barely use this buffer and it can be shrunk, if you care about its impact don't lower this below your total indexes.
```

### [aria_pagecache_buffer_size](https://mariadb.com/kb/en/aria-system-variables/#aria_pagecache_buffer_size)

Index and data buffer for Aria tables, If you use no or very little data in Aria tables. You may reclaim some memory here

```bash
-------- Aria Metrics ------------------------------------------------------------------------------
[--] Aria Storage Engine is enabled.
[OK] Aria pagecache size / total Aria indexes: 128.0M/328.0K # i use a fraction of my aria buffer since i have no aria tables.
[OK] Aria pagecache hit rate: 99.9% (112K cached / 75 reads) # Aria is used internally for MariaDB, so you still want an incredibly high ratio here.
```

## Swappiness

Swappiness is not an SQL variable but part of your system kernel. Swappiness controls how much free memory a server "likes" to have at any given time, and how frequently it shifts data to swapfile to free up memory. Desktop operating systems will have this value set quite high, whereas servers are less aggressive with their swapfile.

Database workloads especially benefit from having their caches stay in memory and will recommend values under 10 for a dedicated database server. 10 is a good compromise for a mixed use server with adequate memory.

If your server is memory starved, leave swapfile aggressive to ensure it is moving memory around as needed.

```bash
joel@METABOX:~/aa_dev$ free -m
              total        used        free      shared  buff/cache   available
Mem:          15998        1903       13372           2         722       13767
Swap:         4096        1404        2691
# Here we can see a lot of memory page (1404MB) sitting in swap while there is free memory (13372MB) available
```

```bash
[root@auth ~]# free -m
              total        used        free      shared  buff/cache   available
Mem:            738         611          59           1          68          35
Swap:          2047        1014        1033
# Here we can see a memory starved server highly utilizing swap already. I wouldn't mess with it too much. (vm.swappiness is 30)
```

```bash
[root@mysql ~]# free -m
              total        used        free      shared  buff/cache   available
Mem:            738         498          95           7         145         120
Swap:          2047         289        1758
# Here we can see a dedicated single use Database Server, Swappiness is 10 here because we have been careful not to starve it of memory and there is low potential to impact other applications
```

```bash
[--] Information about kernel tuning:
...
[--]    vm.swappiness = 30
[xx] Swappiness is < 10.
...
vm.swappiness <= 10 (echo 10 > /proc/sys/vm/swappiness) or vm.swappiness=10 in /etc/sysctl.conf
```

## Max Asynchronous IO

Unless you are still operating on spinning rust (Hard Disk Drives), or an IO-limited VPS, you can likely increase this value. Database workloads appreciate the additional scaling.

```bash
[--] Information about kernel tuning:
[--]    fs.aio-max-nr = 65536
...
fs.aio-max-nr > 1M (echo 1048576 > /proc/sys/fs/aio-max-nr) or fs.aio-max-nr=1048576 in /etc/sysctl.conf
```
