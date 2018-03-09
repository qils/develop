#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import os
import hashlib
from config import UPLOAD_FOLDER
from functools import partial

current_dir = os.path.abspath(os.path.dirname(__file__))


def get_file_md5(f, chunksize=8092):
    h = hashlib.md5()

    while True:
        context = f.read(chunksize)
        if not context:
            break

        h.update(context)

    return h.hexdigest()


def humanize_bytes(bytesize, precision=2):
    abbrev = (
        (1 << 50, 'PB'),
        (1 << 40, 'EB'),
        (1 << 30, 'TB'),
        (1 << 20, 'MB'),
        (1 << 10, 'KB'),
        (1, 'bytes')
    )

    if bytesize == 1:
        return '1 bytes'

    for factor, suffix in abbrev:
        if bytesize >= factor:
            break

    return '%.*f %s' % (precision, bytesize / factor, suffix)

get_file_path = partial(os.path.join, current_dir, UPLOAD_FOLDER)

