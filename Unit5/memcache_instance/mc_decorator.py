#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import inspect


def cache(key_pattern, mc, expire, max_retry):
    print key_pattern, mc, expire, max_retry

    def wrapper(func):
        arg_names, varargs, varkw, defaults = inspect.getargspec(func)
        print arg_names, varargs, varkw, defaults

        def _(*args, **kwargs):
            pass
        return _
    return wrapper


def create_decorator(mc):
    def cache_(key_pattern, expire=0, mc=mc, max_retry=0):
        return cache(key_pattern, mc=mc, expire=expire, max_retry=max_retry)

    return {'cache': cache_}
