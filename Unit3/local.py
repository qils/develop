#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import threading


mydata = threading.local()
mydata.number = 42
print mydata.number
log = []


def f():
    mydata.number = 12
    log.append(mydata.number)
    print log


t = threading.Thread(target=f, args=())
t.start()
print mydata.number

