#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import re
import inspect
from functools import wraps

_formaters = {}


def formater(text):
    return text.format


def format(text, *a, **kw):
    f = _formaters.get(text)
    if not f:
        f = formater(text)
        _formaters[text] = f
    return f(*a, **kw)      # 生成memcached key


def gen_key_factory(key_pattern, arg_names, defaults):
    args = dict(zip(arg_names[-len(defaults):], defaults)) if defaults else {}
    if callable(key_pattern):
        names = inspect.getargspec(key_pattern)

    def gen_key(*a, **kw):
        aa = args.copy()
        aa.update(zip(arg_names, a))
        aa.update(kw)

        key = format(key_pattern, *[aa[n] for n in arg_names], **aa)
        return key and key.replace(' ', '_'), aa

    return gen_key


def cache(key_pattern, mc, expire, max_retry):
    def wrapper(func):
        arg_names, varargs, varkw, defaults = inspect.getargspec(func)
        if varargs or varkw:
            raise Exception('Not support')
        gen_key = gen_key_factory(key_pattern, arg_names, defaults)

        @wraps(func)
        def _(*args, **kwargs):
            key, args = gen_key(*args, **kwargs)

            if not key:
                return func(*args, **kwargs)

            print 'here--->'
            r = mc.get(key)
            if not r:
                r = func(*args, **kwargs)
                mc.set(key, r, expire)
            return r
        _.original_function = func
        return _
    return wrapper


def create_decorator(mc):
    def cache_(key_pattern, expire=0, mc=mc, max_retry=0):
        return cache(key_pattern, mc=mc, expire=expire, max_retry=max_retry)

    return {'cache': cache_}
