#!/usr/bin/env python
# --*-- coding: utf-8 --*--

import pytest


@pytest.fixture
def setup_math():
    import math
    return math


def test_setup_math(setup_math):
    import time
    time.sleep(4)
    assert setup_math.pow(2, 3) == 8.0


class TestClass(object):
    def test_in(self):
        assert 'h' in 'hello'

    def test_two(self, setup_math):
        assert setup_math.ceil(10) == 10


@pytest.fixture(scope='function')
def setup_function(request):
    def teardown_function():
        print 'teardown function is called'

    request.addfinalizer(teardown_function)
    print 'setup_function called'


def test_setup_function(setup_function):
    print 'Test func called'


@pytest.mark.parametrize('test_input, excepted',[
    (1 + 2, 3),
    (2 ** 2, 4)
])
def test_eval(test_input, excepted):
    assert eval(test_input) == excepted
