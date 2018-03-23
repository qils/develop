#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import redis
import random
from datetime import datetime

ACCOUNT_KEY = 'account:active'
now = datetime.utcnow()
r = redis.StrictRedis(host='0.0.0.0', port=6379)
r.flushall()


def record_active(account_id, time_=None):
    if time_ is None:
        time_ = datetime.utcnow()

    p = r.pipeline()
    key = ACCOUNT_KEY
    for arg in ('year', 'month', 'day'):
        key = '{}:{}'.format(key, getattr(time_, arg))
        p.setbit(key, account_id, 1)
    p.execute()


def gen_records(days, population, count):
    for day in range(1, days):
        time_ = datetime(now.year, now.month, day)
        accounts = random.sample(range(population), count)
        for account_id in accounts:
            record_active(account_id, time_)


gen_records(29, 10000, 2000)


print r.bitcount('{}:{}:{}'.format(ACCOUNT_KEY, now.year, now.month))
print r.bitcount('{}:{}:{}:{}'.format(ACCOUNT_KEY, now.year, now.month, now.day))


account_id = 1200
print r.getbit('{}:{}:{}'.format(ACCOUNT_KEY, now.year, now.month), account_id)

account_id = 10001
print r.getbit('{}:{}:{}'.format(ACCOUNT_KEY, now.year, now.month), account_id)


keys = ['{}:{}:{}:{}L'.format(ACCOUNT_KEY, now.year, now.month, day) for day in range(1, 3)]
r.bitop('or', 'destkey', *keys)
print r.bitcount('destkey:or')

r.bitop('and', 'destkey', *keys)
print r.bitcount('destkey:and')
