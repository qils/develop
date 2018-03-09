#!/usr/bin/env python
# --*-- coding: utf-8 --*--

from blinker import signal

started = signal('test-blinker')


def each(round):
    print round


def round_two(round):
    print 'Only: {}'.format(round)


started.connect(each)
started.connect(round_two, sender=2)


for i in range(10):
    started.send(i)
