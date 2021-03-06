#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import unittest
from collections import Counter
from ut_case import TestCounter as TestCounter2


class TestCounter(unittest.TestCase):
    def setUp(self):
        self.c = Counter('abcdefabc')
        print 'Start up ...'

    def runTest(self):
        c = self.c
        self.assertEqual(c, Counter(a=2, b=2, c=2, d=1, e=1, f=1))

    def tearDown(self):
        print 'Test teardown'


class TestDict(unittest.TestCase):
    def setUp(self):
        self.c = dict((('a', 1), ('b', 2)))
        print 'Start up ...'

    def runTest(self):
        c = self.c
        self.assertEqual(c, {'a': 1, 'b': 2})

    def tearDown(self):
        print 'Test teardown'


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestCounter2('test_basics'))
    suite.addTest(TestCounter2('test_update'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
