#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import config
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy import and_, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


eng = create_engine(config.DB_URI)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)


Base.metadata.drop_all(bind=eng)
Base.metadata.create_all(bind=eng)

Session = sessionmaker(bind=eng)
session = Session()


session.add_all([User(name=username) for username in ('mm1', 'mm2', 'mm3')])
session.commit()


def get_result(rs):
    print '-' * 50
    for row in rs:
        print row.id, row.name


rs = session.query(User).all()
get_result(rs)


rs = session.query(User).filter(and_(User.id > 2, User.id < 4))
get_result(rs)
