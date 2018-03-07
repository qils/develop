#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import logging
from logging.handlers import RotatingFileHandler


def log_module(level=logging.WARN):
    formatter = logging.Formatter('[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')
    handler = RotatingFileHandler('slow_query.log', maxBytes=10000, backupCount=10)
    handler.setLevel(level)
    handler.setFormatter(formatter)

    return handler
