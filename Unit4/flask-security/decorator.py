#!/usr/bin/env python
# --*-- coding: utf-8 --*--

from flask import abort
from flask_login import current_user
from functools import wraps
from modules import Permission


def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def _deco(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)

            return func(*args, **kwargs)
        return _deco
    return decorator


def admin_required(func):
    return permission_required(Permission.ADMINSTER)(func)
