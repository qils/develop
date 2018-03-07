#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import config
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, tuple_
from sqlalchemy.sql import select, asc, and_


eng = create_engine(config.DB_URI)
meta = MetaData(eng)

users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('Name', String(50), nullable=False)
)


if users.exists():
    users.drop()
users.create()


def execute(s):
    print '-' * 50
    rs = con.execute(s)

    for row in rs:
        print row['id'], row['Name']


with eng.connect() as con:
    for username in ['mm1', 'mm2', 'mm3']:
        user = users.insert().values(Name=username)
        print str(user)
        con.execute(user)


stm = select([users]).limit(1)
print stm
execute(stm)
