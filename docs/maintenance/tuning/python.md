# Python

## Version Update

Newer versions of python can focus heavily on performance improvements, some more than others. But be aware regressions for stability or security reasons may always be the case.

As a general rule, Python 3.9 and Python 3.11 both had a strong focus on performance improvements. Python 3.12 is looking promising but has yet to have widespread testing, adoption and deployment. A simple comparison is available at [speed.python.org](https://speed.python.org/comparison/?exe=12%2BL%2B3.11%2C12%2BL%2B3.12%2C12%2BL%2B3.10%2C12%2BL%2B3.9%2C12%2BL%2B3.8&ben=746&env=1&hor=false&bas=none&chart=normal+bars).

[Djangobench](https://github.com/django/djangobench/tree/master) is the source of synthetic benchmarks and a useful tool for running comparisons. Below are some examples to inform your investigations.

Keep in mind while a 1.2x faster result is significant, it's only one step of the process, Celery, SQL, Redis, and many other factors will influence the end result, and this _python_ speed improvement will not translate 1:1 into real world performance.

### Running Djangobench

```bash
python3.8 -m venv py38
python3.11 -m venv py311
pip install -e git://github.com/django/djangobench.git#egg=djangobench
git clone https://github.com/django/django.git
cd django
djangobench --control=x --experiment=x --control-python=x --experiment-python=x -r /home/ozira/djangobench/results -t 500
```

### Django 4.2.13 Py38 v Py311

- Djangobench 0.10.0
- Django 4.2.13
- Python 3.8.19 vs Python 3.11.5

```bash
python3.8 -m venv py38
python3.11 -m venv py38
pip install -e git://github.com/django/djangobench.git#egg=djangobench
git clone https://github.com/django/django.git
cd django

ozira@METABOX:~/djangobench/django$ djangobench --control=4.2.13 --experiment=4.2.13 --control-python=/home/ozira/djangobench/py38/bin/python --experiment-python=/home/ozira/djangobench/py311/bin/python -r /home/ozira/djangobench/results -t 500
Running all benchmarks
Recording data to '/home/ozira/djangobench/results'
Control: Django 4.2 (in git branch 4.2)
Experiment: Django 4.2 (in git branch 4.2)

Running 'multi_value_dict' benchmark ...
Min: 0.000016 -> 0.000014: 1.1215x faster
Avg: 0.000212 -> 0.000158: 1.3378x faster
Significant (t=8.313771)
Stddev: 0.00012 -> 0.00008: 1.3703x smaller (N = 500)

Running 'query_values' benchmark ...
Min: 0.000096 -> 0.000083: 1.1540x faster
Avg: 0.000100 -> 0.000087: 1.1391x faster
Significant (t=20.039719)
Stddev: 0.00001 -> 0.00001: 1.0402x smaller (N = 500)

Running 'query_delete' benchmark ...
Min: 0.000089 -> 0.000077: 1.1555x faster
Avg: 0.000094 -> 0.000082: 1.1492x faster
Significant (t=24.020715)
Stddev: 0.00001 -> 0.00001: 1.0738x smaller (N = 500)

Running 'query_select_related' benchmark ...
Min: 0.021098 -> 0.017898: 1.1788x faster
Avg: 0.027279 -> 0.019895: 1.3712x faster
Significant (t=31.103306)
Stddev: 0.00486 -> 0.00213: 2.2832x smaller (N = 500)

Running 'query_aggregate' benchmark ...
Min: 0.000162 -> 0.000140: 1.1626x faster
Avg: 0.000184 -> 0.000153: 1.2025x faster
Significant (t=20.672411)
Stddev: 0.00003 -> 0.00002: 1.2643x smaller (N = 500)

Running 'query_raw_deferred' benchmark ...
Min: 0.005456 -> 0.004688: 1.1637x faster
Avg: 0.006070 -> 0.005151: 1.1786x faster
Significant (t=10.912514)
Stddev: 0.00155 -> 0.00107: 1.4503x smaller (N = 500)

Running 'query_get_or_create' benchmark ...
Min: 0.000526 -> 0.000457: 1.1526x faster
Avg: 0.000597 -> 0.000546: 1.0946x faster
Significant (t=7.469654)
Stddev: 0.00010 -> 0.00012: 1.1192x larger (N = 500)

Running 'query_values_list' benchmark ...
Min: 0.000102 -> 0.000090: 1.1403x faster
Avg: 0.000113 -> 0.000096: 1.1733x faster
Significant (t=13.975856)
Stddev: 0.00002 -> 0.00001: 2.0715x smaller (N = 500)

Running 'url_resolve_flat_i18n_off' benchmark ...
Min: 0.069399 -> 0.058137: 1.1937x faster
Avg: 0.074039 -> 0.064810: 1.1424x faster
Significant (t=21.837249)
Stddev: 0.00341 -> 0.00881: 2.5880x larger (N = 500)

Running 'qs_filter_chaining' benchmark ...
Min: 0.000304 -> 0.000263: 1.1583x faster
Avg: 0.000321 -> 0.000281: 1.1424x faster
Significant (t=15.363420)
Stddev: 0.00003 -> 0.00005: 1.8538x larger (N = 500)

Running 'template_render' benchmark ...
Min: 0.001211 -> 0.000970: 1.2490x faster
Avg: 0.001471 -> 0.001360: 1.0816x faster
Significant (t=2.688854)
Stddev: 0.00067 -> 0.00064: 1.0463x smaller (N = 500)

Running 'query_get' benchmark ...
Min: 0.000340 -> 0.000295: 1.1554x faster
Avg: 0.000382 -> 0.000324: 1.1797x faster
Significant (t=26.055010)
Stddev: 0.00004 -> 0.00003: 1.5530x smaller (N = 500)

Running 'query_none' benchmark ...
Min: 0.000082 -> 0.000074: 1.1133x faster
Avg: 0.000089 -> 0.000081: 1.0934x faster
Significant (t=2.334959)
Stddev: 0.00005 -> 0.00005: 1.0667x larger (N = 500)

Running 'query_complex_filter' benchmark ...
Min: 0.000050 -> 0.000053: 1.0480x slower
Avg: 0.000055 -> 0.000058: 1.0495x slower
Significant (t=-3.073848)
Stddev: 0.00001 -> 0.00001: 1.0593x larger (N = 500)

Running 'query_filter' benchmark ...
Min: 0.000169 -> 0.000157: 1.0758x faster
Avg: 0.000186 -> 0.000173: 1.0756x faster
Significant (t=9.677659)
Stddev: 0.00002 -> 0.00002: 1.0462x smaller (N = 500)

Running 'template_render_simple' benchmark ...
Min: 0.000039 -> 0.000034: 1.1694x faster
Avg: 0.000046 -> 0.000040: 1.1437x faster
Not significant
Stddev: 0.00010 -> 0.00008: 1.2071x smaller (N = 500)

Running 'default_middleware' benchmark ...
Min: -0.000061 -> -0.000088: 0.6901x faster
Avg: 0.000002 -> 0.000001: 2.1933x faster
Not significant
Stddev: 0.00003 -> 0.00002: 1.5573x smaller (N = 500)

Running 'query_annotate' benchmark ...
Min: 0.000237 -> 0.000216: 1.0986x faster
Avg: 0.000279 -> 0.000252: 1.1089x faster
Significant (t=9.006132)
Stddev: 0.00006 -> 0.00004: 1.6353x smaller (N = 500)

Running 'raw_sql' benchmark ...
Min: 0.000021 -> 0.000014: 1.4549x faster
Avg: 0.000022 -> 0.000015: 1.4636x faster
Significant (t=30.661315)
Stddev: 0.00000 -> 0.00000: 2.1050x smaller (N = 500)

Running 'url_resolve_flat' benchmark ...
Min: 0.069107 -> 0.056678: 1.2193x faster
Avg: 0.076299 -> 0.066199: 1.1526x faster
Significant (t=16.072616)
Stddev: 0.00711 -> 0.01212: 1.7039x larger (N = 500)

Running 'l10n_render' benchmark ...
Min: 0.002025 -> 0.001557: 1.3009x faster
Avg: 0.002215 -> 0.001671: 1.3258x faster
Significant (t=23.802622)
Stddev: 0.00045 -> 0.00025: 1.7786x smaller (N = 500)

Running 'query_count' benchmark ...
Min: 0.000145 -> 0.000130: 1.1209x faster
Avg: 0.000165 -> 0.000148: 1.1163x faster
Significant (t=6.919972)
Stddev: 0.00005 -> 0.00003: 1.5444x smaller (N = 500)

Running 'model_delete' benchmark ...
Min: 0.000148 -> 0.000123: 1.2062x faster
Avg: 0.000172 -> 0.000138: 1.2410x faster
Significant (t=27.181750)
Stddev: 0.00002 -> 0.00002: 1.1414x smaller (N = 500)

Running 'query_iterator' benchmark ...
Min: 0.000189 -> 0.000109: 1.7400x faster
Avg: 0.000208 -> 0.000118: 1.7557x faster
Significant (t=49.768122)
Stddev: 0.00003 -> 0.00002: 1.5989x smaller (N = 500)

Running 'template_compilation' benchmark ...
Min: 0.000206 -> 0.000173: 1.1888x faster
Avg: 0.000223 -> 0.000219: 1.0169x faster
Not significant
Stddev: 0.00011 -> 0.00011: 1.0781x smaller (N = 500)

Running 'query_all_multifield' benchmark ...
Min: 0.018550 -> 0.015556: 1.1925x faster
Avg: 0.021732 -> 0.017870: 1.2161x faster
Significant (t=17.544643)
Stddev: 0.00371 -> 0.00324: 1.1438x smaller (N = 500)

Running 'query_prefetch_related' benchmark ...
Min: 0.017945 -> 0.015631: 1.1480x faster
Avg: 0.021111 -> 0.018532: 1.1391x faster
Significant (t=12.174441)
Stddev: 0.00352 -> 0.00316: 1.1143x smaller (N = 500)

Running 'query_all_converters' benchmark ...
Min: 0.000639 -> 0.000543: 1.1774x faster
Avg: 0.000693 -> 0.000583: 1.1878x faster
Significant (t=32.728842)
Stddev: 0.00004 -> 0.00006: 1.4338x larger (N = 500)

Running 'query_distinct' benchmark ...
Min: 0.000132 -> 0.000138: 1.0442x slower
Avg: 0.000138 -> 0.000149: 1.0834x slower
Significant (t=-11.713427)
Stddev: 0.00002 -> 0.00002: 1.0455x larger (N = 500)

Running 'query_dates' benchmark ...
Min: 0.000426 -> 0.000372: 1.1440x faster
Avg: 0.000479 -> 0.000430: 1.1135x faster
Significant (t=15.165974)
Stddev: 0.00005 -> 0.00006: 1.2095x larger (N = 500)

Running 'model_save_existing' benchmark ...
Min: 0.004182 -> 0.003730: 1.1212x faster
Avg: 0.004460 -> 0.004028: 1.1073x faster
Significant (t=33.972394)
Stddev: 0.00019 -> 0.00021: 1.0838x larger (N = 500)

Running 'query_delete_related' benchmark ...
Min: 0.000140 -> 0.000126: 1.1047x faster
Avg: 0.000159 -> 0.000143: 1.1088x faster
Significant (t=3.361755)
Stddev: 0.00006 -> 0.00009: 1.4858x larger (N = 500)

Running 'url_reverse' benchmark ...
Min: 0.000072 -> 0.000099: 1.3810x slower
Avg: 0.000104 -> 0.000112: 1.0749x slower
Not significant
Stddev: 0.00033 -> 0.00008: 3.9995x smaller (N = 500)

Running 'query_latest' benchmark ...
Min: 0.000177 -> 0.000150: 1.1805x faster
Avg: 0.000199 -> 0.000167: 1.1891x faster
Significant (t=16.579351)
Stddev: 0.00003 -> 0.00003: 1.2223x smaller (N = 500)

Running 'form_create' benchmark ...
Min: 0.000018 -> 0.000015: 1.1897x faster
Avg: 0.000024 -> 0.000018: 1.3592x faster
Significant (t=4.264451)
Stddev: 0.00003 -> 0.00002: 1.3397x smaller (N = 500)

Running 'query_update' benchmark ...
Min: 0.000062 -> 0.000047: 1.3306x faster
Avg: 0.000067 -> 0.000053: 1.2660x faster
Significant (t=25.960527)
Stddev: 0.00001 -> 0.00001: 1.2136x larger (N = 500)

Running 'query_in_bulk' benchmark ...
Min: 0.000196 -> 0.000183: 1.0695x faster
Avg: 0.000238 -> 0.000212: 1.1222x faster
Significant (t=9.208556)
Stddev: 0.00005 -> 0.00004: 1.0293x smaller (N = 500)

Running 'url_resolve_nested' benchmark ...
Min: 0.000058 -> 0.000047: 1.2381x faster
Avg: 0.000094 -> 0.000060: 1.5585x faster
Not significant
Stddev: 0.00047 -> 0.00020: 2.2921x smaller (N = 500)

Running 'model_creation' benchmark ...
Min: 0.000086 -> 0.000071: 1.2232x faster
Avg: 0.000096 -> 0.000080: 1.1972x faster
Significant (t=5.528555)
Stddev: 0.00004 -> 0.00005: 1.1460x larger (N = 500)

Running 'query_order_by' benchmark ...
Min: 0.000180 -> 0.000153: 1.1761x faster
Avg: 0.000192 -> 0.000168: 1.1406x faster
Significant (t=14.472948)
Stddev: 0.00002 -> 0.00003: 1.0888x larger (N = 500)

Running 'startup' benchmark ...
Skipped: Django 1.9 and later has changed app loading. This benchmark needs fixing anyway.

Running 'form_clean' benchmark ...
Min: 0.000006 -> 0.000005: 1.2056x faster
Avg: 0.000006 -> 0.000006: 1.1728x faster
Significant (t=5.893457)
Stddev: 0.00000 -> 0.00000: 1.4504x larger (N = 500)

Running 'locale_from_request' benchmark ...
Min: 0.000122 -> 0.000113: 1.0747x faster
Avg: 0.000130 -> 0.000119: 1.0879x faster
Significant (t=2.108857)
Stddev: 0.00009 -> 0.00007: 1.2298x smaller (N = 500)

Running 'query_exists' benchmark ...
Min: 0.000411 -> 0.000351: 1.1700x faster
Avg: 0.000472 -> 0.000406: 1.1616x faster
Significant (t=20.906891)
Stddev: 0.00005 -> 0.00004: 1.2381x smaller (N = 500)

Running 'query_values_10000' benchmark ...
Min: 0.006930 -> 0.006720: 1.0312x faster
Avg: 0.008118 -> 0.007403: 1.0966x faster
Significant (t=8.797671)
Stddev: 0.00137 -> 0.00119: 1.1526x smaller (N = 500)

Running 'query_exclude' benchmark ...
Min: 0.000197 -> 0.000166: 1.1884x faster
Avg: 0.000220 -> 0.000183: 1.2010x faster
Significant (t=22.491738)
Stddev: 0.00003 -> 0.00002: 1.2009x smaller (N = 500)

Running 'query_raw' benchmark ...
Min: 0.006850 -> 0.005836: 1.1739x faster
Avg: 0.007724 -> 0.006518: 1.1851x faster
Significant (t=13.372258)
Stddev: 0.00168 -> 0.00111: 1.5089x smaller (N = 500)

Running 'url_resolve' benchmark ...
Min: 0.006464 -> 0.005129: 1.2602x faster
Avg: 0.006980 -> 0.005578: 1.2512x faster
Significant (t=62.894242)
Stddev: 0.00044 -> 0.00023: 1.8763x smaller (N = 500)

Running 'model_save_new' benchmark ...
Min: 0.004156 -> 0.003608: 1.1519x faster
Avg: 0.004399 -> 0.003921: 1.1220x faster
Significant (t=31.848867)
Stddev: 0.00022 -> 0.00026: 1.1820x larger (N = 500)

Running 'query_all' benchmark ...
Min: 0.009951 -> 0.008729: 1.1399x faster
Avg: 0.011392 -> 0.010135: 1.1240x faster
Significant (t=7.913017)
Stddev: 0.00257 -> 0.00246: 1.0449x smaller (N = 500)
```

### Django 4.2.13 Py311 v Py312

- Djangobench 0.10.0
- Django 4.2.13
- Python 3.11.9 vs Python 3.12.3

```bash
python3.8 -m venv py38
python3.11 -m venv py38
pip install -e git://github.com/django/djangobench.git#egg=djangobench
git clone https://github.com/django/django.git
cd django

ozira@METABOX:~/djangobench/django$ djangobench --control=4.2.13 --experiment=4.2.13 --control-python=/home/ozira/djangobench/py311/bin/python --experiment-python=/home/ozira/djangobench/py312/bin/python -r /home/ozira/djangobench/results -t 500
Running all benchmarks
Recording data to '/home/ozira/djangobench/results'
Control: Django 4.2.13 (in git branch 4.2.13)
Experiment: Django 4.2.13 (in git branch 4.2.13)

Running 'multi_value_dict' benchmark ...
Min: 0.000015 -> 0.000012: 1.2159x faster
Avg: 0.000153 -> 0.000145: 1.0567x faster
Not significant
Stddev: 0.00008 -> 0.00008: 1.0399x smaller (N = 500)

Running 'query_values' benchmark ...
Min: 0.000080 -> 0.000074: 1.0884x faster
Avg: 0.000086 -> 0.000080: 1.0848x faster
Significant (t=9.315400)
Stddev: 0.00001 -> 0.00001: 1.3002x larger (N = 500)

Running 'query_delete' benchmark ...
Min: 0.000076 -> 0.000073: 1.0437x faster
Avg: 0.000082 -> 0.000078: 1.0473x faster
Significant (t=6.287296)
Stddev: 0.00001 -> 0.00001: 1.2237x smaller (N = 500)

Running 'query_select_related' benchmark ...
Min: 0.015799 -> 0.015198: 1.0395x faster
Avg: 0.017664 -> 0.016664: 1.0600x faster
Significant (t=12.493385)
Stddev: 0.00129 -> 0.00124: 1.0404x smaller (N = 500)

Running 'query_aggregate' benchmark ...
Min: 0.000180 -> 0.000170: 1.0605x faster
Avg: 0.000196 -> 0.000202: 1.0290x slower
Significant (t=-3.095949)
Stddev: 0.00002 -> 0.00003: 1.6034x larger (N = 500)

Running 'query_raw_deferred' benchmark ...
Min: 0.004605 -> 0.003799: 1.2122x faster
Avg: 0.005051 -> 0.004491: 1.1246x faster
Significant (t=7.096110)
Stddev: 0.00099 -> 0.00146: 1.4821x larger (N = 500)

Running 'query_get_or_create' benchmark ...
Min: 0.000407 -> 0.000441: 1.0838x slower
Avg: 0.000467 -> 0.000504: 1.0794x slower
Significant (t=-6.031826)
Stddev: 0.00009 -> 0.00010: 1.1220x larger (N = 500)

Running 'query_values_list' benchmark ...
Min: 0.000079 -> 0.000078: 1.0091x faster
Avg: 0.000085 -> 0.000085: 1.0028x slower
Not significant
Stddev: 0.00001 -> 0.00001: 1.5801x larger (N = 500)

Running 'url_resolve_flat_i18n_off' benchmark ...
Min: 0.054191 -> 0.052512: 1.0320x faster
Avg: 0.062988 -> 0.056872: 1.1075x faster
Significant (t=14.068836)
Stddev: 0.00854 -> 0.00465: 1.8373x smaller (N = 500)

Running 'qs_filter_chaining' benchmark ...
Min: 0.000253 -> 0.000233: 1.0868x faster
Avg: 0.000274 -> 0.000251: 1.0890x faster
Significant (t=12.292236)
Stddev: 0.00003 -> 0.00003: 1.2192x smaller (N = 500)

Running 'template_render' benchmark ...
Min: 0.000882 -> 0.000826: 1.0679x faster
Avg: 0.001003 -> 0.000906: 1.1072x faster
Significant (t=3.338298)
Stddev: 0.00054 -> 0.00036: 1.5250x smaller (N = 500)

Running 'query_get' benchmark ...
Min: 0.000280 -> 0.000263: 1.0631x faster
Avg: 0.000303 -> 0.000292: 1.0373x faster
Significant (t=6.991086)
Stddev: 0.00002 -> 0.00002: 1.0173x smaller (N = 500)

Running 'query_none' benchmark ...
Min: 0.000052 -> 0.000050: 1.0482x faster
Avg: 0.000058 -> 0.000056: 1.0345x faster
Not significant
Stddev: 0.00003 -> 0.00006: 1.9705x larger (N = 500)

Running 'query_complex_filter' benchmark ...
Min: 0.000038 -> 0.000035: 1.0815x faster
Avg: 0.000040 -> 0.000037: 1.0691x faster
Significant (t=10.690955)
Stddev: 0.00000 -> 0.00000: 1.3311x larger (N = 500)

Running 'query_filter' benchmark ...
Min: 0.000141 -> 0.000176: 1.2429x slower
Avg: 0.000156 -> 0.000216: 1.3882x slower
Significant (t=-42.392024)
Stddev: 0.00002 -> 0.00003: 1.8049x larger (N = 500)

Running 'template_render_simple' benchmark ...
Min: 0.000030 -> 0.000036: 1.2122x slower
Avg: 0.000035 -> 0.000045: 1.2980x slower
Significant (t=-2.068415)
Stddev: 0.00007 -> 0.00009: 1.3543x larger (N = 500)

Running 'default_middleware' benchmark ...
Min: -0.000159 -> -0.000214: 0.7434x faster
Avg: 0.000001 -> 0.000001: 1.1672x faster
Not significant
Stddev: 0.00002 -> 0.00002: 1.1005x larger (N = 500)

Running 'query_annotate' benchmark ...
Min: 0.000204 -> 0.000198: 1.0298x faster
Avg: 0.000226 -> 0.000236: 1.0459x slower
Significant (t=-4.509109)
Stddev: 0.00003 -> 0.00004: 1.5714x larger (N = 500)

Running 'raw_sql' benchmark ...
Min: 0.000018 -> 0.000013: 1.3404x faster
Avg: 0.000019 -> 0.000015: 1.3195x faster
Significant (t=19.789629)
Stddev: 0.00000 -> 0.00000: 1.3561x smaller (N = 500)

Running 'url_resolve_flat' benchmark ...
Min: 0.055935 -> 0.053402: 1.0474x faster
Avg: 0.062895 -> 0.059771: 1.0523x faster
Significant (t=7.194834)
Stddev: 0.00723 -> 0.00648: 1.1147x smaller (N = 500)

Running 'l10n_render' benchmark ...
Min: 0.001529 -> 0.001251: 1.2219x faster
Avg: 0.001611 -> 0.001377: 1.1701x faster
Significant (t=18.793991)
Stddev: 0.00018 -> 0.00021: 1.1812x larger (N = 500)

Running 'query_count' benchmark ...
Min: 0.000205 -> 0.000190: 1.0786x faster
Avg: 0.000230 -> 0.000223: 1.0340x faster
Significant (t=3.666845)
Stddev: 0.00003 -> 0.00004: 1.3467x larger (N = 500)

Running 'model_delete' benchmark ...
Min: 0.000125 -> 0.000115: 1.0868x faster
Avg: 0.000146 -> 0.000135: 1.0808x faster
Significant (t=7.537652)
Stddev: 0.00003 -> 0.00002: 1.4769x smaller (N = 500)

Running 'query_iterator' benchmark ...
Min: 0.000110 -> 0.000097: 1.1344x faster
Avg: 0.000116 -> 0.000103: 1.1269x faster
Significant (t=19.477018)
Stddev: 0.00001 -> 0.00001: 1.0328x larger (N = 500)

Running 'template_compilation' benchmark ...
Min: 0.000157 -> 0.000157: 1.0038x faster
Avg: 0.000173 -> 0.000169: 1.0255x faster
Not significant
Stddev: 0.00008 -> 0.00008: 1.0180x smaller (N = 500)

Running 'query_all_multifield' benchmark ...
Min: 0.014928 -> 0.014535: 1.0270x faster
Avg: 0.017357 -> 0.016710: 1.0387x faster
Significant (t=3.854898)
Stddev: 0.00263 -> 0.00268: 1.0198x larger (N = 500)

Running 'query_prefetch_related' benchmark ...
Min: 0.014613 -> 0.013929: 1.0491x faster
Avg: 0.016610 -> 0.016188: 1.0261x faster
Significant (t=2.746974)
Stddev: 0.00236 -> 0.00250: 1.0569x larger (N = 500)

Running 'query_all_converters' benchmark ...
Min: 0.000525 -> 0.000493: 1.0659x faster
Avg: 0.000604 -> 0.000527: 1.1458x faster
Significant (t=24.506675)
Stddev: 0.00006 -> 0.00004: 1.7192x smaller (N = 500)

Running 'query_distinct' benchmark ...
Min: 0.000150 -> 0.000181: 1.2049x slower
Avg: 0.000159 -> 0.000231: 1.4503x slower
Significant (t=-31.080159)
Stddev: 0.00002 -> 0.00005: 3.0049x larger (N = 500)

Running 'query_dates' benchmark ...
Min: 0.000512 -> 0.000402: 1.2740x faster
Avg: 0.000677 -> 0.000541: 1.2510x faster
Significant (t=18.130874)
Stddev: 0.00014 -> 0.00009: 1.5731x smaller (N = 500)

Running 'model_save_existing' benchmark ...
Min: 0.004219 -> 0.003506: 1.2033x faster
Avg: 0.005591 -> 0.004282: 1.3058x faster
Significant (t=24.601648)
Stddev: 0.00105 -> 0.00056: 1.8802x smaller (N = 500)

Running 'query_delete_related' benchmark ...
Min: 0.000146 -> 0.000113: 1.2893x faster
Avg: 0.000164 -> 0.000125: 1.3116x faster
Significant (t=11.903195)
Stddev: 0.00006 -> 0.00004: 1.2887x smaller (N = 500)

Running 'url_reverse' benchmark ...
Min: 0.000083 -> 0.000051: 1.6336x faster
Avg: 0.000098 -> 0.000057: 1.7123x faster
Significant (t=9.922770)
Stddev: 0.00008 -> 0.00005: 1.5293x smaller (N = 500)

Running 'query_latest' benchmark ...
Min: 0.000171 -> 0.000149: 1.1500x faster
Avg: 0.000191 -> 0.000167: 1.1440x faster
Significant (t=9.636091)
Stddev: 0.00005 -> 0.00003: 1.6181x smaller (N = 500)

Running 'form_create' benchmark ...
Min: 0.000015 -> 0.000015: 1.0149x slower
Avg: 0.000018 -> 0.000018: 1.0134x faster
Not significant
Stddev: 0.00002 -> 0.00002: 1.0031x smaller (N = 500)

Running 'query_update' benchmark ...
Min: 0.000048 -> 0.000045: 1.0663x faster
Avg: 0.000052 -> 0.000048: 1.0711x faster
Significant (t=7.190354)
Stddev: 0.00001 -> 0.00001: 1.3463x larger (N = 500)

Running 'query_in_bulk' benchmark ...
Min: 0.000161 -> 0.000198: 1.2326x slower
Avg: 0.000176 -> 0.000269: 1.5247x slower
Significant (t=-26.624807)
Stddev: 0.00003 -> 0.00007: 2.2105x larger (N = 500)

Running 'url_resolve_nested' benchmark ...
Min: 0.000063 -> 0.000042: 1.4993x faster
Avg: 0.000082 -> 0.000061: 1.3509x faster
Not significant
Stddev: 0.00027 -> 0.00033: 1.2034x larger (N = 500)

Running 'model_creation' benchmark ...
Min: 0.000079 -> 0.000074: 1.0644x faster
Avg: 0.000089 -> 0.000087: 1.0230x faster
Not significant
Stddev: 0.00005 -> 0.00008: 1.4667x larger (N = 500)

Running 'query_order_by' benchmark ...
Min: 0.000179 -> 0.000162: 1.1071x faster
Avg: 0.000207 -> 0.000183: 1.1311x faster
Significant (t=9.116430)
Stddev: 0.00005 -> 0.00003: 1.6620x smaller (N = 500)

Running 'startup' benchmark ...
Skipped: Django 1.9 and later has changed app loading. This benchmark needs fixing anyway.

Running 'form_clean' benchmark ...
Min: 0.000005 -> 0.000004: 1.1374x faster
Avg: 0.000005 -> 0.000005: 1.1159x faster
Significant (t=3.486468)
Stddev: 0.00000 -> 0.00000: 1.1186x smaller (N = 500)

Running 'locale_from_request' benchmark ...
Min: 0.000126 -> 0.000117: 1.0788x faster
Avg: 0.000141 -> 0.000130: 1.0820x faster
Significant (t=2.168131)
Stddev: 0.00008 -> 0.00008: 1.0548x larger (N = 500)

Running 'query_exists' benchmark ...
Min: 0.000339 -> 0.000270: 1.2522x faster
Avg: 0.000390 -> 0.000302: 1.2915x faster
Significant (t=32.599092)
Stddev: 0.00005 -> 0.00003: 1.6766x smaller (N = 500)

Running 'query_values_10000' benchmark ...
Min: 0.007119 -> 0.005268: 1.3513x faster
Avg: 0.007891 -> 0.006276: 1.2573x faster
Significant (t=18.731021)
Stddev: 0.00120 -> 0.00151: 1.2516x larger (N = 500)

Running 'query_exclude' benchmark ...
Min: 0.000181 -> 0.000157: 1.1532x faster
Avg: 0.000222 -> 0.000173: 1.2822x faster
Significant (t=22.161234)
Stddev: 0.00005 -> 0.00002: 2.4379x smaller (N = 500)

Running 'query_raw' benchmark ...
Min: 0.006000 -> 0.005498: 1.0913x faster
Avg: 0.006669 -> 0.006219: 1.0723x faster
Significant (t=5.713937)
Stddev: 0.00118 -> 0.00130: 1.0984x larger (N = 500)

Running 'url_resolve' benchmark ...
Min: 0.005204 -> 0.004399: 1.1832x faster
Avg: 0.005764 -> 0.004764: 1.2099x faster
Significant (t=38.897887)
Stddev: 0.00055 -> 0.00018: 3.0723x smaller (N = 500)

Running 'model_save_new' benchmark ...
Min: 0.003674 -> 0.003351: 1.0967x faster
Avg: 0.003917 -> 0.003604: 1.0868x faster
Significant (t=21.508370)
Stddev: 0.00021 -> 0.00025: 1.2091x larger (N = 500)

Running 'query_all' benchmark ...
Min: 0.008655 -> 0.008097: 1.0689x faster
Avg: 0.010801 -> 0.009255: 1.1669x faster
Significant (t=8.961354)
Stddev: 0.00304 -> 0.00237: 1.2846x smaller (N = 500)
```

### Python 3.12.3 Dj4.2 vs Dj5.0

This benchmark is purely for development notes.

- Djangobench 0.10.0
- Python 3.12.3
- Django 4.2.13 vs Django 5.0.6

```bash
python3.8 -m venv py38
python3.11 -m venv py38
pip install -e git://github.com/django/djangobench.git#egg=djangobench
git clone https://github.com/django/django.git
cd django

ozira@METABOX:~/djangobench/django$ djangobench --control=4.2.13 --experiment=5.0.6 --control-python=/home/ozira/djangobench/py312/bin/python --experiment-python=/home/ozira/djangobench/py312/bin/python -r /home/ozira/djangobench/results -t 500
Running all benchmarks
Recording data to '/home/ozira/djangobench/results'
Control: Django 4.2.13 (in git branch 4.2.13)
Experiment: Django 5.0.6 (in git branch 5.0.6)

Running 'multi_value_dict' benchmark ...
Min: 0.000013 -> 0.000023: 1.7898x slower
Avg: 0.000159 -> 0.000314: 1.9720x slower
Significant (t=-18.448864)
Stddev: 0.00009 -> 0.00017: 1.8462x larger (N = 500)

Running 'query_values' benchmark ...
Min: 0.000086 -> 0.000093: 1.0836x slower
Avg: 0.000092 -> 0.000101: 1.1016x slower
Significant (t=-13.223024)
Stddev: 0.00001 -> 0.00001: 1.2472x larger (N = 500)

Running 'query_delete' benchmark ...
Min: 0.000098 -> 0.000085: 1.1525x faster
Avg: 0.000109 -> 0.000105: 1.0412x faster
Significant (t=3.610998)
Stddev: 0.00002 -> 0.00002: 1.2485x larger (N = 500)

Running 'query_select_related' benchmark ...
Min: 0.016080 -> 0.017390: 1.0815x slower
Avg: 0.018038 -> 0.020007: 1.1092x slower
Significant (t=-10.013539)
Stddev: 0.00204 -> 0.00390: 1.9094x larger (N = 500)

Running 'query_aggregate' benchmark ...
Min: 0.000195 -> 0.000186: 1.0503x faster
Avg: 0.000225 -> 0.000210: 1.0729x faster
Significant (t=6.534745)
Stddev: 0.00004 -> 0.00004: 1.0807x smaller (N = 500)

Running 'query_raw_deferred' benchmark ...
Min: 0.003904 -> 0.004196: 1.0748x slower
Avg: 0.004346 -> 0.004650: 1.0698x slower
Significant (t=-4.131647)
Stddev: 0.00113 -> 0.00119: 1.0537x larger (N = 500)

Running 'query_get_or_create' benchmark ...
Min: 0.000447 -> 0.000482: 1.0795x slower
Avg: 0.000546 -> 0.000559: 1.0244x slower
Not significant
Stddev: 0.00012 -> 0.00010: 1.1415x smaller (N = 500)

Running 'query_values_list' benchmark ...
Min: 0.000082 -> 0.000085: 1.0385x slower
Avg: 0.000089 -> 0.000093: 1.0418x slower
Significant (t=-4.441191)
Stddev: 0.00001 -> 0.00002: 1.5940x larger (N = 500)

Running 'url_resolve_flat_i18n_off' benchmark ...
Min: 0.054035 -> 0.054465: 1.0079x slower
Avg: 0.062802 -> 0.058801: 1.0680x faster
Significant (t=4.849003)
Stddev: 0.01815 -> 0.00330: 5.4996x smaller (N = 500)

Running 'qs_filter_chaining' benchmark ...
Min: 0.000242 -> 0.000301: 1.2454x slower
Avg: 0.000255 -> 0.000320: 1.2553x slower
Significant (t=-19.514075)
Stddev: 0.00004 -> 0.00006: 1.3907x larger (N = 500)

Running 'template_render' benchmark ...
Min: 0.000849 -> 0.000823: 1.0308x faster
Avg: 0.000985 -> 0.000914: 1.0773x faster
Significant (t=2.995514)
Stddev: 0.00036 -> 0.00038: 1.0474x larger (N = 500)

Running 'query_get' benchmark ...
Min: 0.000283 -> 0.000272: 1.0390x faster
Avg: 0.000325 -> 0.000304: 1.0704x faster
Significant (t=10.235216)
Stddev: 0.00004 -> 0.00003: 1.3055x smaller (N = 500)

Running 'query_none' benchmark ...
Min: 0.000069 -> 0.000093: 1.3482x slower
Avg: 0.000081 -> 0.000103: 1.2714x slower
Significant (t=-3.771605)
Stddev: 0.00011 -> 0.00008: 1.3869x smaller (N = 500)

Running 'query_complex_filter' benchmark ...
Min: 0.000048 -> 0.000039: 1.2131x faster
Avg: 0.000051 -> 0.000042: 1.2180x faster
Significant (t=23.139363)
Stddev: 0.00001 -> 0.00001: 1.1332x smaller (N = 500)

Running 'query_filter' benchmark ...
Min: 0.000143 -> 0.000195: 1.3597x slower
Avg: 0.000162 -> 0.000218: 1.3425x slower
Significant (t=-15.508875)
Stddev: 0.00007 -> 0.00003: 2.6056x smaller (N = 500)

Running 'template_render_simple' benchmark ...
Min: 0.000042 -> 0.000029: 1.4210x faster
Avg: 0.000052 -> 0.000036: 1.4621x faster
Significant (t=2.949575)
Stddev: 0.00010 -> 0.00007: 1.3581x smaller (N = 500)

Running 'default_middleware' benchmark ...
Min: -0.000154 -> -0.000074: 0.4827x slower
Avg: 0.000002 -> 0.000002: 1.5375x slower
Not significant
Stddev: 0.00003 -> 0.00003: 1.0173x smaller (N = 500)

Running 'query_annotate' benchmark ...
Min: 0.000200 -> 0.000204: 1.0182x slower
Avg: 0.000230 -> 0.000245: 1.0629x slower
Significant (t=-7.240006)
Stddev: 0.00003 -> 0.00003: 1.0010x larger (N = 500)

Running 'raw_sql' benchmark ...
Min: 0.000013 -> 0.000015: 1.1728x slower
Avg: 0.000014 -> 0.000016: 1.1890x slower
Significant (t=-9.630569)
Stddev: 0.00000 -> 0.00000: 1.3213x larger (N = 500)

Running 'url_resolve_flat' benchmark ...
Min: 0.054495 -> 0.053987: 1.0094x faster
Avg: 0.059588 -> 0.059220: 1.0062x faster
Not significant
Stddev: 0.00520 -> 0.00563: 1.0816x larger (N = 500)

Running 'l10n_render' benchmark ...
Min: 0.001263 -> 0.000914: 1.3821x faster
Avg: 0.001386 -> 0.001024: 1.3533x faster
Significant (t=29.074072)
Stddev: 0.00020 -> 0.00020: 1.0040x smaller (N = 500)

Running 'query_count' benchmark ...
Min: 0.000178 -> 0.000186: 1.0407x slower
Avg: 0.000196 -> 0.000203: 1.0335x slower
Significant (t=-2.855455)
Stddev: 0.00005 -> 0.00002: 1.9799x smaller (N = 500)

Running 'model_delete' benchmark ...
Min: 0.000124 -> 0.000109: 1.1351x faster
Avg: 0.000144 -> 0.000125: 1.1548x faster
Significant (t=15.819525)
Stddev: 0.00002 -> 0.00002: 1.3262x smaller (N = 500)

Running 'query_iterator' benchmark ...
Min: 0.000099 -> 0.000117: 1.1885x slower
Avg: 0.000104 -> 0.000126: 1.2099x slower
Significant (t=-28.698598)
Stddev: 0.00001 -> 0.00001: 1.3498x larger (N = 500)

Running 'template_compilation' benchmark ...
Min: 0.000150 -> 0.000153: 1.0177x slower
Avg: 0.000162 -> 0.000165: 1.0142x slower
Not significant
Stddev: 0.00009 -> 0.00008: 1.0964x smaller (N = 500)

Running 'query_all_multifield' benchmark ...
Min: 0.015027 -> 0.015956: 1.0618x slower
Avg: 0.016603 -> 0.017869: 1.0763x slower
Significant (t=-7.678978)
Stddev: 0.00252 -> 0.00269: 1.0650x larger (N = 500)

Running 'query_prefetch_related' benchmark ...
Min: 0.014046 -> 0.013922: 1.0089x faster
Avg: 0.015939 -> 0.016489: 1.0346x slower
Significant (t=-3.883798)
Stddev: 0.00227 -> 0.00221: 1.0253x smaller (N = 500)

Running 'query_all_converters' benchmark ...
Min: 0.000544 -> 0.000523: 1.0396x faster
Avg: 0.000598 -> 0.000560: 1.0685x faster
Significant (t=16.329893)
Stddev: 0.00004 -> 0.00004: 1.0470x larger (N = 500)

Running 'query_distinct' benchmark ...
Min: 0.000103 -> 0.000109: 1.0592x slower
Avg: 0.000112 -> 0.000116: 1.0375x slower
Significant (t=-5.586589)
Stddev: 0.00001 -> 0.00001: 1.0100x smaller (N = 500)

Running 'query_dates' benchmark ...
Min: 0.000356 -> 0.000405: 1.1369x slower
Avg: 0.000403 -> 0.000460: 1.1406x slower
Significant (t=-19.572384)
Stddev: 0.00004 -> 0.00005: 1.1089x larger (N = 500)

Running 'model_save_existing' benchmark ...
Min: 0.003422 -> 0.003479: 1.0166x slower
Avg: 0.003788 -> 0.003807: 1.0049x slower
Not significant
Stddev: 0.00021 -> 0.00017: 1.2258x smaller (N = 500)

Running 'query_delete_related' benchmark ...
Min: 0.000114 -> 0.000113: 1.0052x faster
Avg: 0.000127 -> 0.000130: 1.0189x slower
Not significant
Stddev: 0.00005 -> 0.00005: 1.0220x smaller (N = 500)

Running 'url_reverse' benchmark ...
Min: 0.000048 -> 0.000050: 1.0329x slower
Avg: 0.000055 -> 0.000063: 1.1449x slower
Significant (t=-2.155616)
Stddev: 0.00005 -> 0.00007: 1.3065x larger (N = 500)

Running 'query_latest' benchmark ...
Min: 0.000139 -> 0.000143: 1.0305x slower
Avg: 0.000153 -> 0.000157: 1.0231x slower
Significant (t=-2.436627)
Stddev: 0.00002 -> 0.00002: 1.1560x larger (N = 500)

Running 'form_create' benchmark ...
Min: 0.000014 -> 0.000013: 1.0312x faster
Avg: 0.000016 -> 0.000015: 1.0981x faster
Not significant
Stddev: 0.00002 -> 0.00002: 1.1374x larger (N = 500)

Running 'query_update' benchmark ...
Min: 0.000044 -> 0.000045: 1.0237x slower
Avg: 0.000047 -> 0.000049: 1.0507x slower
Significant (t=-5.285934)
Stddev: 0.00001 -> 0.00001: 1.7229x larger (N = 500)

Running 'query_in_bulk' benchmark ...
Min: 0.000164 -> 0.000147: 1.1136x faster
Avg: 0.000191 -> 0.000166: 1.1519x faster
Significant (t=17.531877)
Stddev: 0.00003 -> 0.00002: 1.4907x smaller (N = 500)

Running 'url_resolve_nested' benchmark ...
Min: 0.000047 -> 0.000039: 1.2059x faster
Avg: 0.000066 -> 0.000053: 1.2379x faster
Not significant
Stddev: 0.00035 -> 0.00027: 1.3017x smaller (N = 500)

Running 'model_creation' benchmark ...
Min: 0.000071 -> 0.000075: 1.0607x slower
Avg: 0.000080 -> 0.000085: 1.0648x slower
Not significant
Stddev: 0.00007 -> 0.00004: 1.6986x smaller (N = 500)

Running 'query_order_by' benchmark ...
Min: 0.000144 -> 0.000159: 1.1010x slower
Avg: 0.000160 -> 0.000176: 1.1021x slower
Significant (t=-8.959905)
Stddev: 0.00003 -> 0.00003: 1.0795x larger (N = 500)

Running 'startup' benchmark ...
Skipped: Django 1.9 and later has changed app loading. This benchmark needs fixing anyway.

Running 'form_clean' benchmark ...
Min: 0.000004 -> 0.000004: 1.0084x slower
Avg: 0.000004 -> 0.000004: 1.0378x faster
Not significant
Stddev: 0.00000 -> 0.00000: 1.6388x smaller (N = 500)

Running 'locale_from_request' benchmark ...
Min: 0.000112 -> 0.000107: 1.0460x faster
Avg: 0.000119 -> 0.000115: 1.0323x faster
Not significant
Stddev: 0.00007 -> 0.00006: 1.0659x smaller (N = 500)

Running 'query_exists' benchmark ...
Min: 0.000281 -> 0.000273: 1.0274x faster
Avg: 0.000327 -> 0.000304: 1.0761x faster
Significant (t=8.912446)
Stddev: 0.00005 -> 0.00003: 1.4371x smaller (N = 500)

Running 'query_values_10000' benchmark ...
Min: 0.005139 -> 0.005398: 1.0505x slower
Avg: 0.005799 -> 0.005876: 1.0133x slower
Not significant
Stddev: 0.00117 -> 0.00113: 1.0364x smaller (N = 500)

Running 'query_exclude' benchmark ...
Min: 0.000161 -> 0.000160: 1.0074x faster
Avg: 0.000177 -> 0.000174: 1.0209x faster
Significant (t=3.498767)
Stddev: 0.00002 -> 0.00002: 1.0594x smaller (N = 500)

Running 'query_raw' benchmark ...
Min: 0.005483 -> 0.005660: 1.0323x slower
Avg: 0.006040 -> 0.006549: 1.0843x slower
Significant (t=-6.551792)
Stddev: 0.00110 -> 0.00134: 1.2183x larger (N = 500)

Running 'url_resolve' benchmark ...
Min: 0.004650 -> 0.004575: 1.0164x faster
Avg: 0.005069 -> 0.004889: 1.0370x faster
Significant (t=7.516165)
Stddev: 0.00044 -> 0.00030: 1.4556x smaller (N = 500)

Running 'model_save_new' benchmark ...
Min: 0.003318 -> 0.003369: 1.0154x slower
Avg: 0.003624 -> 0.003783: 1.0437x slower
Significant (t=-9.047954)
Stddev: 0.00026 -> 0.00029: 1.1087x larger (N = 500)

Running 'query_all' benchmark ...
Min: 0.007900 -> 0.008847: 1.1198x slower
Avg: 0.008945 -> 0.010023: 1.1206x slower
Significant (t=-7.386401)
Stddev: 0.00224 -> 0.00237: 1.0590x larger (N = 500)
```
