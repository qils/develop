#!/usr/bin/env python
# --*-- coding: utf-8 --*--

from mc_decorator import create_decorator
from libmc import Client, MC_HASH_MD5, MC_POLL_TIMEOUT, MC_CONNECT_TIMEOUT, MC_RETRY_TIMEOUT


mc = Client(
    [
        '127.0.0.1:11211',
    ],
    do_split=True,
    comp_threshold=0,
    noreply=False,
    prefix=None,
    hash_fn=MC_HASH_MD5,
    failover=False
)

mc.config(MC_POLL_TIMEOUT, 100)
mc.config(MC_CONNECT_TIMEOUT, 300)
mc.config(MC_RETRY_TIMEOUT, 5)


globals().update(create_decorator(mc))
