django-redis-slowlog
==================

Command line support for ./manage.py redisslowlog

A pretty formatter for Redis' [SLOWLOG GET](http://redis.io/commands/slowlog) command

Note: `complexity` is an added feature in the [Garantia Data custom Redis version (Redis Labs' flavor)](https://github.com/RedisLabs/redis). The data was added to the redis-py parsed response in [this pull request](https://github.com/andymccurdy/redis-py/pull/622) (still waiting for merge as of the writing of this script).


## Installation:

Install via pip:

    $ pip install git+git://github.com/loisaidasam/django-redis-slowlog.git

(requires [redis](https://github.com/andymccurdy/redis-py) and [pytz](https://pypi.python.org/pypi/pytz/))

Add "djangoredisslowlog" to your `INSTALLED_APPS` setting (in settings.py) like this:

    INSTALLED_APPS = (
        ...
        'djangoredisslowlog',
    )


## Usage:

    $ ./manage.py redisslowlog
    #          id     duration      start_time                           complexity
    1        7761   1368.070ms 2015-05-28 23:25:16+00:00 (2m ago)
        KEYS celery*
    
    2        7760   1335.585ms 2015-05-28 23:25:26+00:00 (2m ago)
        KEYS foo:bar:*
    
    3        7762    514.646ms 2015-05-28 23:25:03+00:00 (2m ago)            Complexity info: N:517336
        SMEMBERS friends:bart_simpson
