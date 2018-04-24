#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import unittest
from collections import Counter


class TestCounter(unittest.TestCase):
    def setUp(self):
        self.c = Counter('abcdefabc')
        print 'Start up ...'

    def runTest(self):
        c = self.c
        self.assertEqual(c, Counter(a=2, b=2, c=2, d=1, e=1, f=1))

    def tearDown(self):
        print 'Test teardown'


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestCounter())
    runner = unittest.TextTestRunner()
    runner.run(suite)
