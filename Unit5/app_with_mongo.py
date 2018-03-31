#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import datetime
import random
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
client.drop_database('db')
db = client.db


Range = 1440
l = [random.randint(1, 100) for i in range(Range)]


for i in range(Range):
    s = {'metric': 'review_count', 'client_type': 2, 'value': l[i],
         'datetime': datetime.datetime(2018, 03, 31, 0, 0) + datetime.timedelta(minutes=i)}
    db.a.insert_one(s)


for i in range(24):
    s = {'metric': 'review_count', 'client_type': 2, 'datetime': datetime.datetime(2018, 03, 31), 'hour': i}
    s.update({str(k): v for k, v in enumerate(l[60 * i:60 * (i + 1)])})
    db.b.insert_one(s)
