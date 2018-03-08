#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import os
import hashlib

current_dir = os.path.abspath(os.path.dirname(__file__))


def get_file_md5(f, chunksize=8092):
    h = hashlib.md5()

    while True:
        context = f.read(chunksize)
        if not context:
            break

        h.update(context)

    return h.hexdigest()


def humanize_bytes(size, precision=2):
    abbrev = (
        (1 << 50, 'PB'),
        (1 << 40, 'EB'),
        (1 << 30, 'TB'),
        (1 << 20, 'MB'),
        (1 << 10, 'KB'),
        (1, 'bytes')
    )

    if size == 1:
        return '1 bytes'

    ret = next((factor for factor in abbrev if size > factor[0]))
    return '%.*f %s' % (size / ret[0], precision, ret[1])

